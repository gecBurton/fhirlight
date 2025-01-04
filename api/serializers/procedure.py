from api.models.procedure import ProcedureProfile
from api.serializers.common import (
    ProfileSerializer,
)


class ProcedureSerializer(ProfileSerializer):
    class Meta:
        fields = (
            "id",
            "resourceType",
            "code",
            "subject",
            "performedDateTime",
            "status",
        )
        model = ProcedureProfile
