from api.models import DeviceProfile
from api.serializers.common import (
    ProfileSerializer,
)


class DeviceSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype")
        model = DeviceProfile
