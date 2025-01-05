from api.models import EpisodeOfCareProfile
from api.serializers.common import ProfileSerializer


class EpisodeOfCareSerializer(ProfileSerializer):
    class Meta:
        fields = (
            "id",
            "resourceType",
            "status",
            "type",
            "patient",
            "careManager",
            "managingOrganization",
        )
        model = EpisodeOfCareProfile
