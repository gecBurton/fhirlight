from api.models import LocationProfile
from api.serializers.common import (
    ProfileSerializer,
)


class LocationSerializer(ProfileSerializer):
    class Meta:
        exclude = ["created_at", "updated_at", "polymorphic_ctype"]
        model = LocationProfile
