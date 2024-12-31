
from api.models import (
    OrganizationAddress,
    OrganizationIdentifier,
    Organization,
    OrganizationContactPoint,
)
from api.serializers.common import UKCoreModelSerializer, UKCoreProfileSerializer


class OrganizationAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "organization", "created_at", "updated_at")
        model = OrganizationAddress


class OrganizationTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "organization", "created_at", "updated_at")
        model = OrganizationContactPoint


class OrganizationIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "organization", "created_at", "updated_at")
        model = OrganizationIdentifier


class OrganizationSerializer(UKCoreProfileSerializer):
    address = OrganizationAddressSerializer(
        required=False, many=True, source="organizationaddress_set"
    )
    telecom = OrganizationTelecomSerializer(
        required=False, many=True, source="organizationcontactpoint_set"
    )
    identifier = OrganizationIdentifierSerializer(
        required=False, many=True, source="organizationidentifier_set"
    )

    class Meta:
        fields = ("resourceType", "id", "identifier", "name", "address", "telecom")
        model = Organization

    def create(self, validated_data):
        addresses = validated_data.pop("organizationaddress_set", [])
        identifiers = validated_data.pop("organizationidentifier_set", [])
        telecoms = validated_data.pop("organizationcontactpoint_set", [])

        organization = Organization.objects.create(**validated_data)
        for address in addresses:
            OrganizationAddress.objects.create(organization=organization, **address)

        for identifier in identifiers:
            OrganizationIdentifier.objects.create(
                organization=organization, **identifier
            )

        for telecom in telecoms:
            OrganizationContactPoint.objects.create(
                organization=organization, **telecom
            )
        return organization
