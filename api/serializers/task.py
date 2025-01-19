from rest_framework.fields import IntegerField
from rest_framework.serializers import Serializer

from api.models import TaskProfile
from api.serializers.common import PeriodSerializer, ProfileSerializer


class RestrictionSerializer(Serializer):
    period = PeriodSerializer(required=False, source="restrictionPeriod")
    repetitions = IntegerField(required=False, source="restrictionRepetitions")


class TaskSerializer(ProfileSerializer):
    restriction = RestrictionSerializer(required=False, source="*")

    def to_internal_value(self, data):
        data["_for"] = data.pop("for", None)
        return super().to_internal_value(data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["for"] = representation.pop("_for", None)
        return representation

    class Meta:
        exclude = (
            "created_at",
            "restrictionRepetitions",
            "updated_at",
            "polymorphic_ctype",
            "restrictionPeriod",
        )
        model = TaskProfile
