from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models.schedule import ScheduleProfile, ScheduleIdentifier
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class ScheduleIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = ScheduleIdentifier


class planningHorizonSerializer(Serializer):
    start = DateTimeField(required=False, source="planningHorizonStart")
    end = DateTimeField(required=False, source="planningHorizonEnd")


class ScheduleSerializer(ProfileSerializer):
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
        model = ScheduleProfile
