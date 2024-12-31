from rest_framework.fields import (
    CharField,
    SerializerMethodField,
    DateTimeField,
    JSONField,
)
from rest_framework.serializers import ModelSerializer

from api.models import Patient, Organization
from api.models.datatypes import Concept
from api.models.observation import Observation, ObservationComponent
from api.serializers.common import (
    UKCoreModelSerializer,
    ConceptSerializer,
    RelatedResourceSerializer,
)


class ObservationComponentSerializer(ModelSerializer):
    code = ConceptSerializer(
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_OBSERVATION_TYPE
        )
    )
    valueQuantity = JSONField(required=False)

    class Meta:
        fields = ("code", "valueQuantity")
        model = ObservationComponent


class ObservationSerializer(UKCoreModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()
    category = ConceptSerializer(
        many=True,
        required=False,
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
        required=False, many=True, queryset=Organization.objects.all()
    )
    effectiveDateTime = DateTimeField(required=False)
    effectiveInstant = DateTimeField(required=False)

    component = ObservationComponentSerializer(
        many=True, required=False, source="observationcomponent_set"
    )

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
            "effectiveDateTime",
            "effectiveInstant",
            "component",
        )
        model = Observation

    def create(self, validated_data):
        components = validated_data.pop("observationcomponent_set", [])
        performers = validated_data.pop("performer", [])
        categories = validated_data.pop("category", [])

        observation = Observation.objects.create(**validated_data)
        observation.performer.set(performers)
        observation.category.set(categories)
        observation.save()

        for component in components:
            ObservationComponent.objects.create(observation=observation, **component)
        return observation
