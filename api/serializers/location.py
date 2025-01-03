from api.models import Location
from api.models.location import LocationIdentifier, LocationAddress, LocationTelecom
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
)


class LocationIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "location", "created_at", "updated_at")
        model = LocationIdentifier


class LocationAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "created_at", "updated_at")
        model = LocationAddress


class LocationTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "location", "created_at", "updated_at")
        model = LocationTelecom


class LocationSerializer(UKCoreProfileSerializer):
    identifier = LocationIdentifierSerializer(
        many=True, required=False, source="locationidentifier_set"
    )
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
            "identifier",
            "address",
            "type",
            "telecom",
            "managingOrganization",
        ]
        model = Location
