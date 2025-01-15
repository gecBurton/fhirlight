from api.models.schedule import ScheduleProfile
from api.serializers.common import (
    ProfileSerializer,
)


class ScheduleSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = ScheduleProfile
