from rest_framework.fields import (
    CharField,
    DateTimeField,
    JSONField,
)
from rest_framework.serializers import ModelSerializer, Serializer

from api.models.datatypes import Concept
from api.models.observation import (
    Observation,
    ObservationComponent,
    ObservationIdentifier,
)
from api.serializers.common import (
    UKCoreModelSerializer,
    CodingSerializer,
    UKCoreProfileSerializer,
)


class ObservationComponentSerializer(ModelSerializer):
    code = CodingSerializer(valueset=Concept.VALUESET.UK_CORE_OBSERVATION_TYPE)
    valueQuantity = JSONField(required=False)

    class Meta:
        fields = ("code", "valueQuantity")
        model = ObservationComponent


class ObservationIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "observation", "created_at", "updated_at")
        model = ObservationIdentifier


class ReferenceRangeSerializer(Serializer):
    low = DateTimeField(source="batchExpirationDate", required=False)
    high = CharField(source="batchLotNumber", required=False)

    def to_internal_value(self, data):
        raise ValueError(data)


class ObservationSerializer(UKCoreProfileSerializer):
    category = CodingSerializer(
        many=True,
        required=False,
        valueset=Concept.VALUESET.OBSERVATION_CATEGORY_CODE,
    )

    effectiveDateTime = DateTimeField(required=False)
    effectiveInstant = DateTimeField(required=False)

    component = ObservationComponentSerializer(
        many=True, required=False, source="observationcomponent_set"
    )
    identifier = ObservationIdentifierSerializer(
        required=False, many=True, source="observationidentifier_set"
    )
    valueQuantity = JSONField(required=False)

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
            "identifier",
            "valueQuantity",
            "hasMember",
            "bodySite",
        )
        model = Observation
