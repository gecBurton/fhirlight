from rest_framework.fields import URLField, CharField
from rest_framework.serializers import Serializer

from api.models.message_header import MessageHeaderProfile
from api.serializers.common import ProfileSerializer


class MessageHeaderEventCodingSerializer(Serializer):
    code = CharField(source="eventCodingCode")
    display = CharField(required=False, source="eventCodingDisplay")
    system = URLField(required=False, source="eventCodingSystem")


class MessageHeaderSourceSerializer(Serializer):
    endpoint = CharField(source="sourceEndpoint")


class MessageHeaderSerializer(ProfileSerializer):
    eventCoding = MessageHeaderEventCodingSerializer(source="*")
    source = MessageHeaderSourceSerializer(source="*")

    class Meta:
        exclude = [
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "eventCodingCode",
            "sourceEndpoint",
            "eventCodingDisplay",
            "eventCodingSystem",
        ]
        model = MessageHeaderProfile
