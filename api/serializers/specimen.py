from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

from api.models import Patient, Practitioner
from api.models.datatypes import Concept
from api.models.specimen import Specimen
from api.serializers.common import (
    UKCoreProfileSerializer,
    CodingSerializer,
    RelatedResourceSerializer,
)


class SpecimenComponentSerializer(Serializer):
    method = CodingSerializer(valueset=Concept.VALUESET.FHIR_SPECIMEN_COLLECTION_METHOD)
    collector = RelatedResourceSerializer(
        queryset=Practitioner.objects.all(), required=False
    )
    bodySite = CodingSerializer(
        required=False, valueset=Concept.VALUESET.UK_CORE_SPECIMEN_BODY_SITE
    )
    collectedDateTime = DateTimeField(required=False)


class SpecimenSerializer(UKCoreProfileSerializer):
    type = CodingSerializer(
        required=False, valueset=Concept.VALUESET.UK_CORE_SPECIMEN_TYPE
    )
    subject = RelatedResourceSerializer(queryset=Patient.objects.all(), required=False)
    collection = SpecimenComponentSerializer(
        required=False, source="specimencomponent_set"
    )

    collection = SpecimenComponentSerializer(required=False, source="*")

    class Meta:
        fields = (
            "id",
            "resourceType",
            "receivedTime",
            "status",
            "type",
            "subject",
            "collection",
        )
        model = Specimen
