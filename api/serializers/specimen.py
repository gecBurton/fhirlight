from api.models.specimen import UKCoreSpecimen
from api.serializers.common import (
    UKCoreProfileSerializer,
)


class SpecimenCollectionSerializer(UKCoreProfileSerializer):
    class Meta:
        fields = (
            "method",
            "collector",
            "bodySite",
            "collectedDateTime",
        )
        model = UKCoreSpecimen


class SpecimenSerializer(UKCoreProfileSerializer):
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
        model = UKCoreSpecimen
