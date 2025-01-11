from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models.service_request import ServiceRequestProfile
from api.serializers.common import ProfileSerializer


class PeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="occurrencePeriodStart")
    end = DateTimeField(required=False, source="occurrencePeriodEnd")


class ServiceRequestSerializer(ProfileSerializer):
    occurrencePeriod = PeriodSerializer(source="*", required=False)

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "active",
            "occurrencePeriodStart",
            "occurrencePeriodEnd",
        )
        model = ServiceRequestProfile
