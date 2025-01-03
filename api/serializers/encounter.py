from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models import Patient, Organization, Practitioner, Location
from api.models.datatypes import Concept
from api.models.encounter import (
    Encounter,
    EncounterParticipant,
    EncounterLocation,
    EncounterIdentifier,
    EncounterHospitalization,
)
from api.serializers.common import (
    UKCoreProfileSerializer,
    RelatedResourceSerializer,
    CodingSerializer,
    UKCoreModelSerializer,
    CodingSerializerSimple,
)


class PeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="periodStart")
    end = DateTimeField(required=False, source="periodEnd")


class EncounterLocationSerializer(UKCoreModelSerializer):
    location = RelatedResourceSerializer(queryset=Location.objects.all())

    class Meta:
        fields = ("location",)
        model = EncounterLocation


class EncounterIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "encounter", "created_at", "updated_at")
        model = EncounterIdentifier


class EncounterParticipantSerializer(UKCoreModelSerializer):
    individual = RelatedResourceSerializer(queryset=Practitioner.objects.all())
    type = CodingSerializer(valueset=Concept.VALUESET.PARTICIPANT_TYPE, many=True)

    class Meta:
        fields = ("individual", "type")
        model = EncounterParticipant


class EncounterHospitalizationSerializer(UKCoreModelSerializer):
    dischargeDisposition = CodingSerializer(
        valueset=Concept.VALUESET.UK_CORE_DISCHARGE_DESTINATION, required=False
    )

    class Meta:
        fields = ("dischargeDisposition",)
        model = EncounterHospitalization


class EncounterSerializer(UKCoreProfileSerializer):
    hospitalization = EncounterHospitalizationSerializer(
        required=False, source="encounterhospitalization_set"
    )
    klass = CodingSerializerSimple(
        queryset=Concept.objects.filter(valueset=Concept.VALUESET.V3_ACT_ENCOUNTER_CODE)
    )
    type = CodingSerializer(many=True, valueset=Concept.VALUESET.UK_CORE_ENCOUNTER_TYPE)
    subject = RelatedResourceSerializer(queryset=Patient.objects.all(), required=False)
    period = PeriodSerializer(required=False)
    reasonCode = CodingSerializer(
        valueset=Concept.VALUESET.ENCOUNTER_REASON_CODE, required=False, many=True
    )
    serviceProvider = RelatedResourceSerializer(
        queryset=Organization.objects.all(), required=False
    )
    participant = EncounterParticipantSerializer(
        many=True, required=False, source="encounterparticipant_set"
    )
    location = EncounterLocationSerializer(
        many=True, required=False, source="encounterlocation_set"
    )
    identifier = EncounterIdentifierSerializer(
        many=True, required=False, source="encounteridentifier_set"
    )

    def to_internal_value(self, data):
        data["klass"] = data.pop("class", None)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["class"] = representation.pop("klass")
        return representation

    #    'period',

    def create(self, validated_data):
        validated_data.pop("period", None)
        return super().create(validated_data)

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "type",
            "klass",
            "subject",
            "period",
            "reasonCode",
            "location",
            "serviceProvider",
            "status",
            "participant",
            "hospitalization",
        )
        model = Encounter
