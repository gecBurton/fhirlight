from api.models.slot import SlotProfile
from api.serializers.common import (
    ProfileSerializer,
)


class SlotSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = SlotProfile
