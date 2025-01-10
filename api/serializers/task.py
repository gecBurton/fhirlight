from rest_framework.fields import DateTimeField, IntegerField
from rest_framework.serializers import Serializer

from api.models import TaskProfile
from api.models.task import TaskIdentifier, TaskOutput
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class TaskOutputSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = TaskOutput


class ExecutionPeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="executionPeriodStart")
    end = DateTimeField(required=False, source="executionPeriodEnd")


class RestrictionPeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="restrictionPeriodStart")
    end = DateTimeField(required=False, source="restrictionPeriodEnd")


class RestrictionSerializer(Serializer):
    period = RestrictionPeriodSerializer(required=False, source="*")
    repetitions = IntegerField(required=False, source="restrictionRepetitions")


class TaskIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = TaskIdentifier


class TaskSerializer(ProfileSerializer):
    executionPeriod = ExecutionPeriodSerializer(required=False, source="*")
    restriction = RestrictionSerializer(required=False, source="*")
    identifier = TaskIdentifierSerializer(
        required=False, many=True, source="taskidentifier_set"
    )
    output = TaskOutputSerializer(many=True, required=False, source="taskoutput_set")

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
            "restrictionPeriodEnd",
            "restrictionPeriodStart",
            "restrictionRepetitions",
            "executionPeriodStart",
            "executionPeriodEnd",
            "active",
            "updated_at",
            "polymorphic_ctype",
        )
        model = TaskProfile
