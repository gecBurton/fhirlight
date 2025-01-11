from api.models.operation_outcome import OperationOutcomeProfile
from api.serializers.common import (
    ProfileSerializer,
)


class OperationOutcomeSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype", "active")
        model = OperationOutcomeProfile
