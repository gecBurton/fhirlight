from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models.encounter import (
    Encounter,
    EncounterParticipant,
    EncounterLocation,
    EncounterIdentifier,
    EncounterHospitalization,
)
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
)


class PeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="periodStart")
    end = DateTimeField(required=False, source="periodEnd")


class EncounterLocationSerializer(UKCoreModelSerializer):
    class Meta:
        fields = ("location",)
        model = EncounterLocation


class EncounterIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "encounter", "created_at", "updated_at")
        model = EncounterIdentifier


class EncounterParticipantSerializer(UKCoreModelSerializer):
    class Meta:
        fields = ("individual", "type")
        model = EncounterParticipant


class EncounterHospitalizationSerializer(UKCoreModelSerializer):
    class Meta:
        fields = ("dischargeDisposition",)
        model = EncounterHospitalization


class EncounterSerializer(UKCoreProfileSerializer):
    hospitalization = EncounterHospitalizationSerializer(
        required=False, source="encounterhospitalization_set"
    )
    period = PeriodSerializer(required=False)
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
