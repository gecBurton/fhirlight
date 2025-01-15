from api.models.medication_dispense import (
    MedicationDispenseProfile,
)
from api.serializers.common import (
    ProfileSerializer,
)


class MedicationDispenseSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = MedicationDispenseProfile
