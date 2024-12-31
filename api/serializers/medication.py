from rest_framework.fields import (
    CharField,
    DateTimeField,
)
from rest_framework.serializers import Serializer

from api.models.datatypes import Concept
from api.models.medication import Medication
from api.serializers.common import ConceptSerializer, UKCoreProfileSerializer


class BatchSerializer(Serializer):
    expirationDate = DateTimeField(source="batchExpirationDate", required=False)
    lotNumber = CharField(source="batchLotNumber", required=False)


class MedicationSerializer(UKCoreProfileSerializer):
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
