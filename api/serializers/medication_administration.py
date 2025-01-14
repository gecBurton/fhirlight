from rest_framework.fields import (
    IntegerField,
    CharField,
    URLField,
)
from rest_framework.serializers import Serializer

from api.models import MedicationAdministrationProfile
from api.models.datatypes import Concept
from api.serializers.common import ProfileSerializer, RelatedResourceSerializer


class RateQuantitySerializer(Serializer):
    value = IntegerField(source="rateQuantityValue", required=False)
    unit = CharField(source="rateQuantityUnit", required=False)
    system = URLField(source="rateQuantitySystem", required=False)
    code = CharField(source="rateQuantityCode", required=False)


class DoseSerializer(Serializer):
    value = IntegerField(source="dosageDoseQuantityValue", required=False)
    unit = CharField(source="dosageDoseQuantityUnit", required=False)
    system = URLField(source="dosageDoseQuantitySystem", required=False)
    code = CharField(source="dosageDoseQuantityCode", required=False)


class DosageSerializer(Serializer):
    text = CharField(required=False, source="dosageText")
    site = RelatedResourceSerializer(
        required=False,
        queryset=Concept.objects.filter(valueset=Concept.VALUESET.UK_CORE_BODY_SITE),
        source="dosageSite",
    )
    route = RelatedResourceSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_SUBSTANCE_OR_PRODUCT_ADMINISTRATION_ROUTE
        ),
        source="dosageRoute",
    )
    method = RelatedResourceSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_MEDICATION_DOSAGE_METHOD
        ),
        source="dosageMethod",
    )
    rateQuantity = RateQuantitySerializer(source="*", required=False)
    dose = DoseSerializer(source="*", required=False)


class MedicationAdministrationSerializer(ProfileSerializer):
    dosage = DosageSerializer(source="*", required=False)

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "dosageText",
            "dosageSite",
            "dosageRoute",
            "dosageMethod",
            "dosageRateQuantityValue",
            "dosageRateQuantityUnit",
            "dosageRateQuantitySystem",
            "dosageRateQuantityCode",
            "dosageDoseQuantityValue",
            "dosageDoseQuantityUnit",
            "dosageDoseQuantitySystem",
            "dosageDoseQuantityCode",
        )
        model = MedicationAdministrationProfile
