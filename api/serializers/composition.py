from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import Serializer

from api.models import CompositionProfile
from api.models.composition import CompositionSection
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class IdentifierSerializer(Serializer):
    value = CharField(required=False, source="identifierValue")
    system = SerializerMethodField()

    def get_system(self, _obj):
        return "https://tools.ietf.org/html/rfc4122"


class CompositionSectionSerializer(BaseModelSerializer):
    class Meta:
        fields = ("title", "code", "entry")
        model = CompositionSection


class CompositionSerializer(ProfileSerializer):
    identifier = IdentifierSerializer(source="*", required=False)
    section = CompositionSectionSerializer(
        many=True, required=False, source="compositionsection_set"
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "status",
            "type",
            "date",
            "title",
            "subject",
            "author",
            "encounter",
            "custodian",
            "section",
        )
        model = CompositionProfile
