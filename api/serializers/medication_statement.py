from rest_framework.fields import DateTimeField
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
    QuantitySerializer,
    TimingSerializer,
)


class MedicationStatementDosageDoseAndRateSerializer(BaseModelSerializer):
    doseQuantity = QuantitySerializer(required=False)
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
            "dosage",
        )
        model = MedicationStatementDosageDoseAndRate


class DosageSerializer(BaseModelSerializer):
    timing = TimingSerializer(required=False)
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
        )
        model = MedicationStatementDosage


class EffectivePeriodSerializer(Serializer):
    start = DateTimeField(source="effectivePeriodStart", required=False)
    end = DateTimeField(source="effectivePeriodEnd", required=False)


class MedicationStatementSerializer(ProfileSerializer):
    dosage = DosageSerializer(
        required=False, many=True, source="medicationstatementdosage_set"
    )
    effectivePeriod = EffectivePeriodSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "effectivePeriodEnd",
            "effectivePeriodStart",
        )
        model = MedicationStatementProfile
