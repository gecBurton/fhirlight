from api.models import ImagingStudyProfile
from api.models.datatypes import Concept
from api.models.imaging_study import ImagingStudySeries, ImagingStudySeriesInstance
from api.serializers.common import (
    BaseModelSerializer,
    ConceptModelSerializer,
    ProfileSerializer,
)


class ImagingStudySeriesInstanceSerializer(BaseModelSerializer):
    sopClass = ConceptModelSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.B5_STANDARD_SOP_CLASSES
        ),
    )

    class Meta:
        fields = ("uid", "sopClass", "number", "title")
        model = ImagingStudySeriesInstance


class ImagingStudySeriesSerializer(BaseModelSerializer):
    modality = ConceptModelSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.CID_29_ACQUISITION_MODALITY
        ),
    )
    bodySite = ConceptModelSerializer(
        required=False,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.SNOMED_CT_BODY_STRUCTURES
        ),
    )

    instance = ImagingStudySeriesInstanceSerializer(
        required=False, many=True, source="imagingstudyseriesinstance_set"
    )

    class Meta:
        fields = (
            "uid",
            "number",
            "numberOfInstances",
            "description",
            "modality",
            "bodySite",
            "instance",
        )
        model = ImagingStudySeries


class ImagingStudySerializer(ProfileSerializer):
    series = ImagingStudySeriesSerializer(
        required=False, many=True, source="imagingstudyseries_set"
    )

    class Meta:
        exclude = ["created_at", "updated_at", "polymorphic_ctype"]
        model = ImagingStudyProfile
