from api.models import AppointmentProfile
from api.models.appointment import AppointmentIdentifier, AppointmentParticipant
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class AppointmentIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "appointment", "created_at", "updated_at")
        model = AppointmentIdentifier


class AppointmentParticipantSerializer(BaseModelSerializer):
    class Meta:
        fields = ("type", "actor", "required", "status")
        model = AppointmentParticipant


class AppointmentSerializer(ProfileSerializer):
    identifier = AppointmentIdentifierSerializer(
        many=True, required=False, source="appointmentidentifier_set"
    )
    participant = AppointmentParticipantSerializer(
        many=True, required=False, source="appointmentparticipant_set"
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "status",
            "serviceCategory",
            "serviceType",
            "specialty",
            "appointmentType",
            "priority",
            "description",
            "start",
            "end",
            "created",
            "comment",
            "patientInstruction",
            "reasonReference",
            "basedOn",
            "participant",
        )
        model = AppointmentProfile
