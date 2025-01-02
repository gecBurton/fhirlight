from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models import Location
from api.models.datatypes import Concept
from api.models.schedule import Schedule, ScheduleIdentifier
from api.serializers.common import (
    UKCoreProfileSerializer,
    CodingSerializer,
    RelatedResourceSerializer,
    UKCoreModelSerializer,
)


class ScheduleIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "schedule", "created_at", "updated_at")
        model = ScheduleIdentifier


class planningHorizonSerializer(Serializer):
    start = DateTimeField(required=False, source="planningHorizonStart")
    end = DateTimeField(required=False, source="planningHorizonEnd")


class ScheduleSerializer(UKCoreProfileSerializer):
    serviceCategory = CodingSerializer(
        many=True, required=False, valueset=Concept.VALUESET.SERVICE_CATEGORY
    )
    serviceType = CodingSerializer(
        many=True, required=False, valueset=Concept.VALUESET.SERVICE_TYPE
    )
    specialty = CodingSerializer(
        many=True,
        required=False,
        valueset=Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE,
    )
    actor = RelatedResourceSerializer(
        many=True, required=False, queryset=Location.objects.all()
    )
    identifier = ScheduleIdentifierSerializer(
        many=True, required=False, source="scheduleidentifier_set"
    )
    planningHorizon = planningHorizonSerializer(required=False, source="*")

    class Meta:
        fields = (
            "id",
            "resourceType",
            "active",
            "identifier",
            "planningHorizon",
            "comment",
            "serviceCategory",
            "serviceType",
            "specialty",
            "actor",
        )
        model = Schedule
