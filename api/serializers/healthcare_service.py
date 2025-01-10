from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models import HealthcareServiceProfile
from api.models.healthcare_service import (
    HealthcareServiceTelecom,
    HealthcareServiceIdentifier,
    HealthcareServiceAvailableTime,
    HealthcareServiceNotAvailable,
)
from api.serializers.common import BaseModelSerializer, ProfileSerializer


class HealthcareServiceTelecomSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = HealthcareServiceTelecom


class HealthcareServiceIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = HealthcareServiceIdentifier


class HealthcareServiceAvailableTimeSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = HealthcareServiceAvailableTime


class DurationSerializer(Serializer):
    start = DateTimeField(required=False, source="duringStart")
    end = DateTimeField(required=False, source="duringEnd")


class HealthcareServiceNotAvailableSerializer(BaseModelSerializer):
    during = DurationSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "uuid",
            "profile",
            "created_at",
            "updated_at",
            "duringEnd",
            "duringStart",
        )
        model = HealthcareServiceNotAvailable


class HealthcareServiceSerializer(ProfileSerializer):
    telecom = HealthcareServiceTelecomSerializer(
        many=True, required=False, source="healthcareservicetelecom_set"
    )
    identifier = HealthcareServiceIdentifierSerializer(
        many=True, required=False, source="healthcareserviceidentifier_set"
    )
    availableTime = HealthcareServiceAvailableTimeSerializer(
        many=True, required=False, source="healthcareserviceavailabletime_set"
    )
    notAvailable = HealthcareServiceNotAvailableSerializer(
        many=True, required=False, source="healthcareservicenotavailable_set"
    )

    class Meta:
        exclude = ("created_at", "polymorphic_ctype", "updated_at")
        model = HealthcareServiceProfile
