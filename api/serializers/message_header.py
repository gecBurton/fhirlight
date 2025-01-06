from rest_framework.fields import URLField, CharField
from rest_framework.serializers import Serializer

from api.models.message_header import MessageHeaderProfile, MessageHeaderDestination
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class MessageHeaderDestinationSerializer(BaseModelSerializer):
    class Meta:
        fields = ("receiver", "endpoint")
        model = MessageHeaderDestination


class MessageHeaderEventCodingSerializer(Serializer):
    code = CharField(source="eventCodingCode")
    display = CharField(required=False, source="eventCodingDisplay")
    system = URLField(required=False, source="eventCodingSystem")


class MessageHeaderSourceSerializer(Serializer):
    endpoint = CharField(source="sourceEndpoint")


class MessageHeaderSerializer(ProfileSerializer):
    eventCoding = MessageHeaderEventCodingSerializer(source="*")
    destination = MessageHeaderDestinationSerializer(
        many=True, required=False, source="messageheaderdestination_set"
    )
    source = MessageHeaderSourceSerializer(source="*")

    class Meta:
        fields = (
            "id",
            "resourceType",
            "eventCoding",
            "focus",
            "source",
            "sender",
            "destination",
        )
        model = MessageHeaderProfile
