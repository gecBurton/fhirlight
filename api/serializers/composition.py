from api.models import CompositionProfile
from api.serializers.common import ProfileSerializer


class CompositionSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "active",
        )
        model = CompositionProfile
