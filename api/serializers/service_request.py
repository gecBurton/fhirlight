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
        fields = [
            "resourceType",
            "id",
            "status",
            "basedOn",
            "intent",
            "occurrencePeriod",
            "authoredOn",
            "subject",
            "encounter",
            "requester",
            "performer",
            "locationReference",
            "reasonReference",
            "supportingInfo",
            "patientInstruction",
            "code",
            "reasonCode",
            "category",
            "locationCode",
        ]
        model = ServiceRequestProfile
