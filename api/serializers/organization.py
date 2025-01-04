from api.models import (
    OrganizationAddress,
    OrganizationIdentifier,
    OrganizationProfile,
    OrganizationContactPoint,
)
from api.serializers.common import BaseModelSerializer, ProfileSerializer


class OrganizationAddressSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "organization", "created_at", "updated_at")
        model = OrganizationAddress


class OrganizationTelecomSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "organization", "created_at", "updated_at")
        model = OrganizationContactPoint


class OrganizationIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "organization", "created_at", "updated_at")
        model = OrganizationIdentifier


class OrganizationSerializer(ProfileSerializer):
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
        model = OrganizationProfile
