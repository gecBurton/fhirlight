from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models.flag import FlagProfile, FlagIdentifier
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class PeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="periodStart")
    end = DateTimeField(required=False, source="periodEnd")


class FlagIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = FlagIdentifier


class FlagSerializer(ProfileSerializer):
    period = PeriodSerializer(required=False, source="*")
    identifier = FlagIdentifierSerializer(
        many=True, required=False, source="flagidentifier_set"
    )

    class Meta:
        exclude = (
            "periodStart",
            "periodEnd",
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "active",
        )
        model = FlagProfile
