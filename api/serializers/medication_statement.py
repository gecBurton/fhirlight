from api.models import MedicationStatementProfile
from api.serializers.common import (
    ProfileSerializer,
)


class MedicationStatementSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = MedicationStatementProfile
