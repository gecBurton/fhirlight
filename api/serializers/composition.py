from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import Serializer

from api.models import CompositionProfile
from api.serializers.common import ProfileSerializer


class IdentifierSerializer(Serializer):
    value = CharField(required=False, source="identifierValue")
    system = SerializerMethodField()

    def get_system(self, _obj):
        return "https://tools.ietf.org/html/rfc4122"


class CompositionSerializer(ProfileSerializer):
    identifier = IdentifierSerializer(source="*", required=False)

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "identifierValue",
            "active",
        )
        model = CompositionProfile
