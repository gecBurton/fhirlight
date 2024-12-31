
from api.models import (
    Practitioner,
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
        model = Practitioner

    def create(self, validated_data):
        addresses = validated_data.pop("practitioneraddress_set", [])
        names = validated_data.pop("practitionername_set", [])
        identifiers = validated_data.pop("practitioneridentifier_set", [])
        telecoms = validated_data.pop("practitionertelecom_set", [])

        practitioner = Practitioner.objects.create(**validated_data)

        for address in addresses:
            PractitionerAddress.objects.create(practitioner=practitioner, **address)

        for name in names:
            PractitionerName.objects.create(practitioner=practitioner, **name)

        for identifier in identifiers:
            PractitionerIdentifier.objects.create(
                practitioner=practitioner, **identifier
            )

        for telecom in telecoms:
            PractitionerTelecom.objects.create(practitioner=practitioner, **telecom)
        return practitioner
