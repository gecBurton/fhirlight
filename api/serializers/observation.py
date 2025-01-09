from rest_framework.fields import (
    DateTimeField,
    JSONField,
)

from api.models.observation import (
    ObservationProfile,
    ObservationComponent,
    ObservationIdentifier,
    ObservationReferenceRange,
)
from api.serializers.common import (
    BaseModelSerializer,
    ProfileSerializer,
)


class ObservationComponentSerializer(BaseModelSerializer):
    valueQuantity = JSONField(required=False)

    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = ObservationComponent


class ObservationIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = ObservationIdentifier


class ObservationReferenceRangeSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = ObservationReferenceRange


class ObservationSerializer(ProfileSerializer):
    effectiveDateTime = DateTimeField(required=False)
    effectiveInstant = DateTimeField(required=False)

    component = ObservationComponentSerializer(
        many=True, required=False, source="observationcomponent_set"
    )
    identifier = ObservationIdentifierSerializer(
        required=False, many=True, source="observationidentifier_set"
    )
    valueQuantity = JSONField(required=False)
    referenceRange = ObservationReferenceRangeSerializer(
        many=True, required=False, source="observationreferencerange_set"
    )

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
            "referenceRange",
            "specimen",
        )
        model = ObservationProfile
