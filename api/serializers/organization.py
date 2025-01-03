from api.models import (
    OrganizationAddress,
    OrganizationIdentifier,
    UKCoreOrganization,
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
        model = UKCoreOrganization
