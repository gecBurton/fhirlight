from api.models.observation import (
    ObservationProfile,
)
from api.serializers.common import (
    ProfileSerializer,
)


class ObservationSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = ObservationProfile
