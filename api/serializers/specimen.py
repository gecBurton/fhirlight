from rest_framework.serializers import ModelSerializer

from api.models import Specimen, Patient, Practitioner
from api.models.datatypes import Concept
from api.models.specimen import SpecimenComponent
from api.serializers.common import (
    UKCoreProfileSerializer,
    ConceptSerializer,
    RelatedResourceSerializer,
)


class SpecimenComponentSerializer(ModelSerializer):
    method = ConceptSerializer(
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.FHIR_SPECIMEN_COLLECTION_METHOD
        )
    )
    collector = RelatedResourceSerializer(
        queryset=Practitioner.objects.all(), required=False
    )
    bodySite = ConceptSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_SPECIMEN_BODY_SITE
        ),
    )

    class Meta:
        fields = ("method", "collector", "collectedDateTime", "bodySite")
        model = SpecimenComponent


class SpecimenSerializer(UKCoreProfileSerializer):
    type = ConceptSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_SPECIMEN_TYPE
        ),
    )
    subject = RelatedResourceSerializer(queryset=Patient.objects.all(), required=False)
    collection = SpecimenComponentSerializer(required=False)

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
