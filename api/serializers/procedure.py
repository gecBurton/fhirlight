from api.models.procedure import ProcedureProfile
from api.serializers.common import (
    ProfileSerializer,
)


class ProcedureSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype", "active")
        model = ProcedureProfile
