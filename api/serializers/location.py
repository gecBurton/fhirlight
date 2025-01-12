from api.models import LocationProfile
from api.models.location import LocationAddress
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class LocationAddressSerializer(BaseModelSerializer):
    # required as this is a 1:1 relationship
    class Meta:
        exclude = ("uuid", "created_at", "updated_at")
        model = LocationAddress


class LocationSerializer(ProfileSerializer):
    address = LocationAddressSerializer(required=False)

    class Meta:
        exclude = ["created_at", "updated_at", "polymorphic_ctype", "active"]
        model = LocationProfile
