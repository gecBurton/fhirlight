from rest_framework.fields import (
    DateTimeField,
    JSONField,
)

from api.models.observation import (
    ObservationProfile,
)
from api.serializers.common import (
    ProfileSerializer,
)


class ObservationSerializer(ProfileSerializer):
    effectiveDateTime = DateTimeField(required=False)
    effectiveInstant = DateTimeField(required=False)

    valueQuantity = JSONField(required=False)

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = ObservationProfile
