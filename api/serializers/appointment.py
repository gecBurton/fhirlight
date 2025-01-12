from api.models import AppointmentProfile
from api.models.appointment import AppointmentParticipant
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class AppointmentParticipantSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = AppointmentParticipant


class AppointmentSerializer(ProfileSerializer):
    participant = AppointmentParticipantSerializer(
        many=True, required=False, source="appointmentparticipant_set"
    )

    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype", "active")
        model = AppointmentProfile
