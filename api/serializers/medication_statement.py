from rest_framework.fields import IntegerField, CharField, URLField, DateTimeField
from rest_framework.serializers import Serializer

from api.models import MedicationStatementProfile
from api.models.datatypes import Concept
from api.models.medication_statement import (
    MedicationStatementDosage,
    MedicationStatementDosageDoseAndRate,
)
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
    RelatedResourceSerializer,
)


class DoseQuantitySerializer(Serializer):
    value = IntegerField(source="doseQuantityValue", required=False)
    unit = CharField(source="doseQuantityUnit", required=False)
    system = URLField(source="doseQuantitySystem", required=False)
    code = CharField(source="doseQuantityCode", required=False)


class MedicationStatementDosageDoseAndRateSerializer(BaseModelSerializer):
    doseQuantity = DoseQuantitySerializer(source="*", required=False)
    asNeededCodeableConcept = RelatedResourceSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.AS_NEEDED_CODEABLE_CONCEPT
        ),
    )

    class Meta:
        exclude = (
            "uuid",
            "created_at",
            "updated_at",
            "doseQuantityValue",
            "doseQuantityUnit",
            "doseQuantitySystem",
            "doseQuantityCode",
            "dosage",
        )
        model = MedicationStatementDosageDoseAndRate


class RepeatSerializer(Serializer):
    frequency = IntegerField(source="timingRepeatFrequency")
    period = IntegerField(source="timingRepeatPeriod")
    periodUnit = CharField(source="timingRepeatPeriodUnit")


class TimingSerializer(Serializer):
    repeat = RepeatSerializer(required=False, source="*")


class DosageSerializer(BaseModelSerializer):
    timing = TimingSerializer(required=False, source="*")
    doseAndRate = MedicationStatementDosageDoseAndRateSerializer(
        required=False,
        many=True,
        source="medicationstatementdosagedoseandrate_set",
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
        model = MedicationStatementDosage


class EffectivePeriodSerializer(Serializer):
    start = DateTimeField(source="effectivePeriodStart", required=False)
    end = DateTimeField(source="effectivePeriodEnd", required=False)


class MedicationStatementSerializer(ProfileSerializer):
    dosage = DosageSerializer(
        required=False, many=True, source="medicationstatementdosage_set"
    )
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
