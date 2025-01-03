from api.models import (
    UKCorePractitioner,
    PractitionerName,
    PractitionerIdentifier,
    PractitionerTelecom,
    PractitionerAddress,
)
from api.serializers.common import UKCoreModelSerializer, UKCoreProfileSerializer


class PractitionerNameSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner", "created_at", "updated_at")
        model = PractitionerName


class PractitionerAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner", "created_at", "updated_at")
        model = PractitionerAddress


class PractitionerTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner", "created_at", "updated_at")
        model = PractitionerTelecom


class PractitionerIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner", "created_at", "updated_at")
        model = PractitionerIdentifier


class PractitionerSerializer(UKCoreProfileSerializer):
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
        model = UKCorePractitioner
