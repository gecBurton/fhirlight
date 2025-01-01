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
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return LocationAddress.objects.create(**internal_value)

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
    type = ConceptSerializer(
        required=False,
        many=True,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.SERVICE_DELIVERY_LOCATION_ROLE_TYPE
        ),
    )
    telecom = LocationTelecomSerializer(
        required=False, many=True, source="locationtelecom_set"
    )
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

    def create(self, validated_data):
        identifiers = validated_data.pop("locationidentifier_set", [])
        telecoms = validated_data.pop("locationtelecom_set", [])
        types = validated_data.pop("type", [])

        location = Location.objects.create(**validated_data)

        location.type.set(types)

        for identifier in identifiers:
            LocationIdentifier.objects.create(location=location, **identifier)
        for telecom in telecoms:
            LocationTelecom.objects.create(location=location, **telecom)
        return location
