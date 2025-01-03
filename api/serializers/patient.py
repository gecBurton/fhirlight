from rest_framework.serializers import Serializer, RelatedField

from api.models import UKCorePatient
from api.models.datatypes import Concept
from api.models.patient import (
    PatientIdentifier,
    PatientTelecom,
    PatientName,
    PatientAddress,
)
from api.serializers.common import (
    UKCoreModelSerializer,
    UKCoreProfileSerializer,
    ConceptSerializer,
)

from django.utils.translation import gettext_lazy as _


class PatientIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientIdentifier


class PatientAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientAddress


class PatientTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientTelecom


class PatientNameSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientName


class LanguageSerializer(Serializer):
    coding = ConceptSerializer(many=True)


class PatientCommunicationSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_format": _(
            'Incorrect format. Expected {"language": {"coding": [{"code": code]}}.'
        ),
    }

    def to_internal_value(self, data):
        try:
            code = data["language"]["coding"][0]["code"]
        except (KeyError, IndexError):
            self.fail("incorrect_format")

        try:
            return self.get_queryset().get(code=code)
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=code)

    def to_representation(self, value):
        return {
            "language": {
                "coding": [
                    {
                        "code": value.code,
                        "system": value.system,
                        "display": value.display,
                    }
                ]
            }
        }


class PatientSerializer(UKCoreProfileSerializer):
    identifier = PatientIdentifierSerializer(
        required=False, many=True, source="patientidentifier_set"
    )
    address = PatientAddressSerializer(
        required=False, many=True, source="patientaddress_set"
    )
    telecom = PatientTelecomSerializer(
        required=False, many=True, source="patienttelecom_set"
    )
    name = PatientNameSerializer(required=False, many=True, source="patientname_set")

    communication = PatientCommunicationSerializer(
        required=False,
        many=True,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_HUMAN_LANGUAGE
        ),
    )

    class Meta:
        fields = [
            "id",
            "resourceType",
            "gender",
            "identifier",
            "address",
            "telecom",
            "name",
            "birthDate",
            "communication",
        ]
        model = UKCorePatient
