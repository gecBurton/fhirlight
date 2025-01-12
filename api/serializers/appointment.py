from api.models import AppointmentProfile
from api.serializers.common import ProfileSerializer


class AppointmentSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype", "active")
        model = AppointmentProfile
