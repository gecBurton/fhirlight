from rest_framework.fields import (
    CharField,
    DateTimeField,
    JSONField,
)
from rest_framework.serializers import Serializer

from api.models.observation import (
    UKCoreObservation,
    ObservationComponent,
    ObservationIdentifier,
)
from api.serializers.common import (
    UKCoreModelSerializer,
    UKCoreProfileSerializer,
)


class ObservationComponentSerializer(UKCoreModelSerializer):
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
        model = UKCoreObservation
