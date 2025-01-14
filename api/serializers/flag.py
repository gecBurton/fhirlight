from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models.flag import FlagProfile
from api.serializers.common import ProfileSerializer


class PeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="periodStart")
    end = DateTimeField(required=False, source="periodEnd")


class FlagSerializer(ProfileSerializer):
    period = PeriodSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "periodStart",
            "periodEnd",
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = FlagProfile
