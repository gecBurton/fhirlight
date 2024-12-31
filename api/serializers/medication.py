from rest_framework.fields import (
    CharField,
    SerializerMethodField,
    DateTimeField,
)
from rest_framework.relations import RelatedField
from rest_framework.serializers import Serializer

from api.models.datatypes import Concept
from api.models.medication import Medication
from api.serializers.common import UKCoreModelSerializer
from django.utils.translation import gettext_lazy as _


class MedicationFormSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_format": _(
            'Incorrect format. Expected {"language": {"coding": [{"code": code]}}.'
        ),
    }

    def to_internal_value(self, data):
        try:
            code = data["coding"][0]["code"]
        except (KeyError, IndexError):
            self.fail("incorrect_format")

        try:
            return self.get_queryset().get(code=code)
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=code)

    def to_representation(self, value):
        return {
            "coding": [
                {
                    "code": value.code,
                    "system": value.system,
                    "display": value.display,
                }
            ]
        }


class BatchSerializer(Serializer):
    expirationDate = DateTimeField(source="batchExpirationDate", required=False)
    lotNumber = CharField(source="batchLotNumber", required=False)


class MedicationSerializer(UKCoreModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()
    batch = BatchSerializer(required=False, source="*")

    code = MedicationFormSerializer(
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_MEDICATION_CODE
        ),
    )
    form = MedicationFormSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_MEDICATION_FORM
        ),
    )

    class Meta:
        fields = [
            "id",
            "resourceType",
            "code",
            "form",
            "batch",
        ]
        model = Medication

    def get_resourceType(self, _obj):
        return "Medication"
