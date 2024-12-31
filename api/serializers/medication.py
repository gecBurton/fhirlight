from rest_framework.fields import (
    CharField,
    SerializerMethodField,
    DateTimeField,
)
from rest_framework.serializers import Serializer

from api.models.datatypes import Concept
from api.models.medication import Medication
from api.serializers.common import UKCoreModelSerializer, ConceptSerializer


class BatchSerializer(Serializer):
    expirationDate = DateTimeField(source="batchExpirationDate", required=False)
    lotNumber = CharField(source="batchLotNumber", required=False)


class MedicationSerializer(UKCoreModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()
    batch = BatchSerializer(required=False, source="*")

    code = ConceptSerializer(
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_MEDICATION_CODE
        ),
    )
    form = ConceptSerializer(
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
