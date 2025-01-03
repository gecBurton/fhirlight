from api.models.datatypes import Concept
from api.models.immunization import Immunization
from api.serializers.common import (
    UKCoreProfileSerializer,
    CodingSerializer,
)


class ImmunizationSerializer(UKCoreProfileSerializer):
    vaccineCode = CodingSerializer(valueset=Concept.VALUESET.UK_CORE_VACCINE_CODE)

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
        model = Immunization
