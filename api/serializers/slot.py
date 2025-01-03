from api.models.slot import UKCoreSlot, SlotIdentifier
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
)


class SlotIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "slot", "created_at", "updated_at")
        model = SlotIdentifier


class SlotSerializer(UKCoreProfileSerializer):
    identifier = SlotIdentifierSerializer(
        many=True, required=False, source="slotidentifier_set"
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "comment",
            "serviceCategory",
            "serviceType",
            "specialty",
            "appointmentType",
            "start",
            "end",
            "status",
        )
        model = UKCoreSlot
