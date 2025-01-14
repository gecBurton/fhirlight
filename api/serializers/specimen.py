from api.models.specimen import SpecimenProfile
from api.serializers.common import (
    ProfileSerializer,
)


class SpecimenCollectionSerializer(ProfileSerializer):
    class Meta:
        fields = (
            "method",
            "collector",
            "bodySite",
            "collectedDateTime",
        )
        model = SpecimenProfile


class SpecimenSerializer(ProfileSerializer):
    collection = SpecimenCollectionSerializer(required=False, source="*")

    class Meta:
        exclude = [
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "collector",
            "method",
            "bodySite",
            "collectedDateTime",
        ]
        model = SpecimenProfile
