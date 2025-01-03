from rest_framework.fields import (
    CharField,
    DateTimeField,
)
from rest_framework.serializers import Serializer

from api.models.medication import UKCoreMedication
from api.serializers.common import UKCoreProfileSerializer


class BatchSerializer(Serializer):
    expirationDate = DateTimeField(source="batchExpirationDate", required=False)
    lotNumber = CharField(source="batchLotNumber", required=False)


class MedicationSerializer(UKCoreProfileSerializer):
    batch = BatchSerializer(required=False, source="*")

    class Meta:
        fields = [
            "id",
            "resourceType",
            "code",
            "form",
            "batch",
        ]
        model = UKCoreMedication
