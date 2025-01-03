from api.models import UKCoreRelatedPerson
from api.models.related_person import (
    RelatedPersonAddress,
    RelatedPersonTelecom,
    RelatedPersonName,
)
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
)


class RelatedPersonAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "related_person", "created_at", "updated_at")
        model = RelatedPersonAddress


class RelatedPersonTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "related_person", "created_at", "updated_at")
        model = RelatedPersonTelecom


class RelatedPersonNameSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "related_person", "created_at", "updated_at")
        model = RelatedPersonName


class RelatedPersonSerializer(UKCoreProfileSerializer):
    name = RelatedPersonNameSerializer(
        required=False, many=True, source="relatedpersonname_set"
    )
    telecom = RelatedPersonTelecomSerializer(required=False, many=True)
    address = RelatedPersonAddressSerializer(required=False, many=True)

    class Meta:
        fields = (
            "id",
            "resourceType",
            "patient",
            "relationship",
            "name",
            "telecom",
            "address",
        )
        model = UKCoreRelatedPerson
