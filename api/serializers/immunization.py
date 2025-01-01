from api.models import Location, Patient, Organization
from api.models.datatypes import Concept
from api.models.immunization import Immunization
from api.serializers.common import (
    UKCoreProfileSerializer,
    RelatedResourceSerializer,
    CodingSerializer,
)


class ImmunizationSerializer(UKCoreProfileSerializer):
    location = RelatedResourceSerializer(
        required=False, queryset=Location.objects.all()
    )
    manufacturer = RelatedResourceSerializer(
        required=False, queryset=Organization.objects.all()
    )
    patient = RelatedResourceSerializer(queryset=Patient.objects.all())
    vaccineCode = CodingSerializer(
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
        model = Immunization
