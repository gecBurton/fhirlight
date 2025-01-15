from api.models.flag import FlagProfile
from api.serializers.common import ProfileSerializer


class FlagSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = FlagProfile
