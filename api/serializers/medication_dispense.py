from rest_framework.fields import (
    IntegerField,
    CharField,
    URLField,
)
from rest_framework.serializers import Serializer

from api.models.medication_dispense import (
    MedicationDispenseProfile,
    MedicationDispenseDosageInstruction,
)
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
    TimingSerializer,
)


class DosageInstructionSerializer(BaseModelSerializer):
    timing = TimingSerializer(required=False)

    class Meta:
        exclude = (
            "uuid",
            "profile",
            "created_at",
            "updated_at",
        )
        model = MedicationDispenseDosageInstruction


class daysSupplySerializer(Serializer):
    value = IntegerField(source="daysSupplyValue", required=False)
    unit = CharField(source="daysSupplyUnit", required=False)
    system = URLField(source="daysSupplySystem", required=False)
    code = CharField(source="daysSupplyCode", required=False)


class quantitySerializer(Serializer):
    value = IntegerField(source="quantityValue", required=False)
    unit = CharField(source="quantityUnit", required=False)
    system = URLField(source="quantitySystem", required=False)
    code = CharField(source="quantityCode", required=False)


class MedicationDispenseSerializer(ProfileSerializer):
    dosageInstruction = DosageInstructionSerializer(
        required=False, many=True, source="medicationdispensedosageinstruction_set"
    )
    daysSupply = daysSupplySerializer(required=False, source="*")
    quantity = quantitySerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "daysSupplyValue",
            "daysSupplyUnit",
            "daysSupplySystem",
            "daysSupplyCode",
            "quantityCode",
            "quantitySystem",
            "quantityUnit",
            "quantityValue",
        )
        model = MedicationDispenseProfile
