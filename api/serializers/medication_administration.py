from rest_framework.fields import (
    CharField,
)
from rest_framework.serializers import Serializer

from api.models import MedicationAdministrationProfile
from api.models.datatypes import Concept
from api.serializers.common import (
    ProfileSerializer,
    QuantitySerializer,
    RelatedResourceSerializer,
)


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
    rateQuantity = QuantitySerializer(source="dosageRateQuantity", required=False)
    dose = QuantitySerializer(source="dosageDose", required=False)


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
            "dosageDose",
        )
        model = MedicationAdministrationProfile
