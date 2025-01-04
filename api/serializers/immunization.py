from api.models.datatypes import Concept
from api.models.immunization import ImmunizationProfile
from api.serializers.common import (
    ProfileSerializer,
    RelatedResourceSerializer,
)


class ImmunizationSerializer(ProfileSerializer):
    vaccineCode = RelatedResourceSerializer(
        queryset=Concept.objects.filter(valueset=Concept.VALUESET.UK_CORE_VACCINE_CODE)
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "manufacturer",
            "occurrenceDateTime",
            "status",
            "location",
            "patient",
            "vaccineCode",
        )
        model = ImmunizationProfile
