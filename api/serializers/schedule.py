from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models.schedule import ScheduleProfile
from api.serializers.common import (
    ProfileSerializer,
)


class PlanningHorizonSerializer(Serializer):
    start = DateTimeField(required=False, source="planningHorizonStart")
    end = DateTimeField(required=False, source="planningHorizonEnd")


class ScheduleSerializer(ProfileSerializer):
    planningHorizon = PlanningHorizonSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "planningHorizonStart",
            "planningHorizonEnd",
        )
        model = ScheduleProfile
