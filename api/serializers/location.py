from api.models import Location, Organization
from api.models.datatypes import Concept
from api.models.location import LocationIdentifier, LocationAddress, LocationTelecom
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
    ConceptSerializer,
    RelatedResourceSerializer,
)


class LocationIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "location", "created_at", "updated_at")
        model = LocationIdentifier


class LocationAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "location", "created_at", "updated_at")
        model = LocationAddress


class LocationTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "location", "created_at", "updated_at")
        model = LocationTelecom


class LocationSerializer(UKCoreProfileSerializer):
    identifier = LocationIdentifierSerializer(many=True, required=False)
    address = LocationAddressSerializer(required=False)
    type = ConceptSerializer(
        required=False,
        many=True,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.SERVICE_DELIVERY_LOCATION_ROLE_TYPE
        ),
    )
    telecom = LocationTelecomSerializer(required=False, many=True)
    managingOrganization = RelatedResourceSerializer(
        queryset=Organization.objects.all(), required=False
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
