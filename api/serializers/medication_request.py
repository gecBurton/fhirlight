from rest_framework.fields import (
    BooleanField,
    IntegerField,
    CharField,
)
from rest_framework.serializers import Serializer

from api.models import MedicationRequestProfile
from api.models.medication_request import (
    MedicationRequestDosageInstruction,
    MedicationRequestDosageInstructionDoseAndRate,
)
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class MedicationRequestDosageInstructionDoseAndRateSerializer(BaseModelSerializer):
    class Meta:
        exclude = (
            "uuid",
            "dosageInstruction",
            "created_at",
            "updated_at",
        )
        model = MedicationRequestDosageInstructionDoseAndRate


class RepeatSerializer(Serializer):
    frequency = IntegerField(source="timingRepeatFrequency")
    period = IntegerField(source="timingRepeatPeriod")
    periodUnit = CharField(source="timingRepeatPeriodUnit")


class TimingSerializer(Serializer):
    repeat = RepeatSerializer(required=False, source="*")


class DosageInstructionSerializer(BaseModelSerializer):
    timing = TimingSerializer(required=False, source="*")
    doseAndRate = MedicationRequestDosageInstructionDoseAndRateSerializer(
        required=False,
        many=True,
        source="medicationrequestdosageinstructiondoseandrate_set",
    )

    class Meta:
        exclude = (
            "uuid",
            "profile",
            "created_at",
            "updated_at",
            "timingRepeatFrequency",
            "timingRepeatPeriod",
            "timingRepeatPeriodUnit",
        )
        model = MedicationRequestDosageInstruction


class SubstitutionSerializer(Serializer):
    allowedBoolean = BooleanField(required=False, source="substitutionAllowedBoolean")


class MedicationRequestSerializer(ProfileSerializer):
    dosageInstruction = DosageInstructionSerializer(
        many=True, required=False, source="medicationrequestdosageinstruction_set"
    )
    substitution = SubstitutionSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "substitutionAllowedBoolean",
        )
        model = MedicationRequestProfile
