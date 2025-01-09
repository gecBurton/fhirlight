from api.models import DeviceProfile
from api.models.device import DeviceIdentifier
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class DeviceIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = DeviceIdentifier


class DeviceSerializer(ProfileSerializer):
    identifier = DeviceIdentifierSerializer(
        many=True, required=False, source="deviceidentifier_set"
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "status",
            "type",
            "owner",
            "location",
        )
        model = DeviceProfile
