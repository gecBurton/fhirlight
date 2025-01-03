from api.models.specimen import Specimen
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
        model = Specimen


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
        model = Specimen
