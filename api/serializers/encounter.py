from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models.datatypes import Concept
from api.models.encounter import (
    EncounterProfile,
    EncounterParticipant,
    EncounterLocation,
)
from api.serializers.common import (
    ProfileSerializer,
    ConceptModelSerializer,
    RelatedResourceSerializer,
    BaseModelSerializer,
)


class PeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="periodStart")
    end = DateTimeField(required=False, source="periodEnd")


class EncounterHospitalizationSerializer(Serializer):
    dischargeDisposition = RelatedResourceSerializer(
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_DISCHARGE_DESTINATION
        ),
        required=False,
        source="hospitalizationDischargeDisposition",
    )


class EncounterParticipantSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = EncounterParticipant


class EncounterLocationSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = EncounterLocation


class EncounterSerializer(ProfileSerializer):
    klass = ConceptModelSerializer(
        queryset=Concept.objects.filter(valueset=Concept.VALUESET.V3_ACT_ENCOUNTER_CODE)
    )
    participant = EncounterParticipantSerializer(
        many=True, required=False, source="encounterparticipant_set"
    )
    location = EncounterLocationSerializer(
        many=True, required=False, source="encounterlocation_set"
    )
    hospitalization = EncounterHospitalizationSerializer(required=False, source="*")
    period = PeriodSerializer(required=False, source="*")

    def to_internal_value(self, data):
        data["klass"] = data.pop("class", None)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["class"] = representation.pop("klass", None)
        return representation

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "active",
            "hospitalizationDischargeDisposition",
            "periodStart",
            "periodEnd",
        )
        model = EncounterProfile
