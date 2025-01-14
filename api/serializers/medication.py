from rest_framework.fields import (
    CharField,
    DateTimeField,
)
from rest_framework.serializers import Serializer

from api.models.medication import MedicationProfile
from api.serializers.common import ProfileSerializer


class BatchSerializer(Serializer):
    expirationDate = DateTimeField(source="batchExpirationDate", required=False)
    lotNumber = CharField(source="batchLotNumber", required=False)


class MedicationSerializer(ProfileSerializer):
    batch = BatchSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "batchExpirationDate",
            "batchLotNumber",
        )
        model = MedicationProfile
