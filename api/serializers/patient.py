from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import Serializer, RelatedField

from api.models import Patient
from api.models.datatypes import Concept
from api.models.patient import (
    PatientIdentifier,
    PatientTelecom,
    PatientName,
    PatientAddress,
)
from api.serializers.common import UKCoreModelSerializer


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
    def to_internal_value(self, data):
        code = data["language"]["coding"][0]["code"]
        return self.get_queryset().get(code=code)

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


class PatientSerializer(UKCoreModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()
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
        queryset=Concept.objects.filter(system=Concept.SYSTEM.LANGUAGE),
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

    def get_resourceType(self, _obj):
        return "Patient"

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
