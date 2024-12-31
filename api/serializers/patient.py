from rest_framework.fields import CharField
from rest_framework.serializers import Serializer, RelatedField

from api.models import Patient
from api.models.datatypes import Concept
from api.models.patient import (
    PatientIdentifier,
    PatientTelecom,
    PatientName,
    PatientAddress,
)
from api.serializers.common import UKCoreModelSerializer, UKCoreProfileSerializer

from django.utils.translation import gettext_lazy as _


class PatientIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientIdentifier


class PatientAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientAddress


class PatientTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientTelecom


class PatientNameSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "patient", "created_at", "updated_at")
        model = PatientName


class CodingSerializer(Serializer):
    system = CharField()
    code = CharField()
    display = CharField()


class LanguageSerializer(Serializer):
    coding = CodingSerializer(many=True)


class PatientCommunicationSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_format": _(
            'Incorrect format. Expected {"language": {"coding": [{"code": code]}}.'
        ),
    }

    def to_internal_value(self, data):
        try:
            code = data["language"]["coding"][0]["code"]
        except (KeyError, IndexError):
            self.fail("incorrect_format")

        try:
            return self.get_queryset().get(code=code)
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=code)

    def to_representation(self, value):
        return {
            "language": {
                "coding": [
                    {
                        "code": value.code,
                        "system": value.system,
                        "display": value.display,
                    }
                ]
            }
        }


class PatientSerializer(UKCoreProfileSerializer):
    identifier = PatientIdentifierSerializer(
        required=False, many=True, source="patientidentifier_set"
    )
    address = PatientAddressSerializer(
        required=False, many=True, source="patientaddress_set"
    )
    telecom = PatientTelecomSerializer(
        required=False, many=True, source="patienttelecom_set"
    )
    name = PatientNameSerializer(required=False, many=True, source="patientname_set")

    communication = PatientCommunicationSerializer(
        required=False,
        many=True,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_HUMAN_LANGUAGE
        ),
    )

    class Meta:
        fields = [
            "id",
            "resourceType",
            "gender",
            "identifier",
            "address",
            "telecom",
            "name",
            "birthDate",
            "communication",
        ]
        model = Patient

    def create(self, validated_data):
        addresses = validated_data.pop("patientaddress_set", [])
        names = validated_data.pop("patientname_set", [])
        identifiers = validated_data.pop("patientidentifier_set", [])
        telecoms = validated_data.pop("patienttelecom_set", [])
        communications = validated_data.pop("communication", [])

        patient = Patient.objects.create(**validated_data)

        for address in addresses:
            PatientAddress.objects.create(patient=patient, **address)

        for name in names:
            PatientName.objects.create(patient=patient, **name)

        for identifier in identifiers:
            PatientIdentifier.objects.create(patient=patient, **identifier)

        for telecom in telecoms:
            PatientTelecom.objects.create(patient=patient, **telecom)

        patient.communication.set(communications)
        patient.save()
        return patient
