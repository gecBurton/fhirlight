from rest_framework.fields import IntegerField, CharField, URLField, DateTimeField
from rest_framework.serializers import Serializer

from api.models import MedicationStatementProfile
from api.serializers.common import (
    ProfileSerializer,
)


class DoseQuantitySerializer(Serializer):
    value = IntegerField(source="doseQuantityValue", required=False)
    unit = CharField(source="doseQuantityUnit", required=False)
    system = URLField(source="doseQuantitySystem", required=False)
    code = CharField(source="doseQuantityCode", required=False)


# class MedicationStatementDosageInstructionDoseAndRateSerializer(BaseModelSerializer):
#     doseQuantity = DoseQuantitySerializer(source="*", required=False)
#
#     class Meta:
#         exclude = (
#             "uuid",
#             "dosageInstruction",
#             "created_at",
#             "updated_at",
#             "doseQuantityValue",
#             "doseQuantityUnit",
#             "doseQuantitySystem",
#             "doseQuantityCode",
#         )
#         model = MedicationStatementDosageInstructionDoseAndRate


class RepeatSerializer(Serializer):
    frequency = IntegerField(source="timingRepeatFrequency")
    period = IntegerField(source="timingRepeatPeriod")
    periodUnit = CharField(source="timingRepeatPeriodUnit")


class TimingSerializer(Serializer):
    repeat = RepeatSerializer(required=False, source="*")


# class DosageInstructionSerializer(BaseModelSerializer):
#     timing = TimingSerializer(required=False, source="*")
#     doseAndRate = MedicationStatementDosageInstructionDoseAndRateSerializer(
#         required=False,
#         many=True,
#         source="medicationstatementdosageinstructiondoseandrate_set",
#     )
#
#     class Meta:
#         exclude = (
#             "uuid",
#             "profile",
#             "created_at",
#             "updated_at",
#             "timingRepeatFrequency",
#             "timingRepeatPeriod",
#             "timingRepeatPeriodUnit",
#         )
#         model = MedicationStatementDosageInstruction


class EffectivePeriodSerializer(Serializer):
    start = DateTimeField(source="effectivePeriodStart", required=False)
    end = DateTimeField(source="effectivePeriodEnd", required=False)


class MedicationStatementSerializer(ProfileSerializer):
    # dosageInstruction = DosageInstructionSerializer(
    #     required=False, many=True, source="medicationdispensedosageinstruction_set"
    # )
    # daysSupply = daysSupplySerializer(required=False, source="*")
    # quantity = quantitySerializer(required=False, source="*")
    effectivePeriod = EffectivePeriodSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "active",
            "effectivePeriodEnd",
            "effectivePeriodStart",
            # "daysSupplyValue",
            # "daysSupplyUnit",
            # "daysSupplySystem",
            # "daysSupplyCode",
            # "quantityCode",
            # "quantitySystem",
            # "quantityUnit",
            # "quantityValue",
        )
        model = MedicationStatementProfile
