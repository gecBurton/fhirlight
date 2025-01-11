from api.models import LocationProfile
from api.models.location import LocationAddress, LocationTelecom
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class LocationAddressSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "created_at", "updated_at")
        model = LocationAddress


class LocationTelecomSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = LocationTelecom


class LocationSerializer(ProfileSerializer):
    address = LocationAddressSerializer(required=False)
    telecom = LocationTelecomSerializer(
        required=False, many=True, source="locationtelecom_set"
    )

    class Meta:
        fields = [
            "id",
            "resourceType",
            "status",
            "name",
            "address",
            "type",
            "telecom",
            "managingOrganization",
        ]
        model = LocationProfile
