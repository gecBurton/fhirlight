from api.models import RelatedPersonProfile
from api.models.related_person import (
    RelatedPersonAddress,
    RelatedPersonTelecom,
    RelatedPersonName,
)
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class RelatedPersonAddressSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = RelatedPersonAddress


class RelatedPersonTelecomSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = RelatedPersonTelecom


class RelatedPersonNameSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = RelatedPersonName


class RelatedPersonSerializer(ProfileSerializer):
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
        model = RelatedPersonProfile
