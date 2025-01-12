from api.models import EpisodeOfCareProfile
from api.serializers.common import ProfileSerializer


class EpisodeOfCareSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype", "active")
        model = EpisodeOfCareProfile
