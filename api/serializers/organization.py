from api.models import (
    OrganizationProfile,
)
from api.serializers.common import ProfileSerializer


class OrganizationSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = OrganizationProfile
