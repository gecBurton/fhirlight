from rest_framework.fields import CharField, SerializerMethodField, DateTimeField

from api.models import Patient, Organization
from api.models.datatypes import Concept
from api.models.observation import Observation
from api.serializers.common import (
    UKCoreModelSerializer,
    ConceptSerializer,
    RelatedResourceSerializer,
)


class ObservationSerializer(UKCoreModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()
    category = ConceptSerializer(
        many=True,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.OBSERVATION_CATEGORY_CODE,
        ),
    )
    code = ConceptSerializer(
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_OBSERVATION_TYPE,
        ),
    )

    subject = RelatedResourceSerializer(queryset=Patient.objects.all())
    performer = RelatedResourceSerializer(
        many=True, queryset=Organization.objects.all()
    )
    effective = DateTimeField(source="effectiveDateTime", required=False)

    def get_resourceType(self, _obj):
        return "Observation"

    class Meta:
        fields = (
            "id",
            "resourceType",
            "category",
            "code",
            "status",
            "subject",
            "performer",
            "effective",
        )
        model = Observation
