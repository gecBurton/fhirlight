from api.models.slot import SlotProfile, SlotIdentifier
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class SlotIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = SlotIdentifier


class SlotSerializer(ProfileSerializer):
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
        model = SlotProfile
