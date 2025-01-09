from api.models import (
    PractitionerProfile,
    PractitionerName,
    PractitionerIdentifier,
    PractitionerTelecom,
    PractitionerAddress,
)
from api.serializers.common import BaseModelSerializer, ProfileSerializer


class PractitionerNameSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = PractitionerName


class PractitionerAddressSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = PractitionerAddress


class PractitionerTelecomSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = PractitionerTelecom


class PractitionerIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = PractitionerIdentifier


class PractitionerSerializer(ProfileSerializer):
    name = PractitionerNameSerializer(
        required=False, many=True, source="practitionername_set"
    )
    telecom = PractitionerTelecomSerializer(
        required=False, many=True, source="practitionertelecom_set"
    )
    identifier = PractitionerIdentifierSerializer(
        required=False, many=True, source="practitioneridentifier_set"
    )
    address = PractitionerAddressSerializer(
        required=False, many=True, source="practitioneraddress_set"
    )

    class Meta:
        fields = (
            "resourceType",
            "id",
            "identifier",
            "name",
            "address",
            "gender",
            "name",
            "telecom",
        )
        model = PractitionerProfile
