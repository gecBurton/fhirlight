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
        fields = (
            "id",
            "resourceType",
            "receivedTime",
            "status",
            "type",
            "subject",
            "collection",
        )
        model = SpecimenProfile
