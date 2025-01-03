from api.models.procedure import UKCoreProcedure
from api.serializers.common import (
    UKCoreProfileSerializer,
)


class ProcedureSerializer(UKCoreProfileSerializer):
    class Meta:
        fields = (
            "id",
            "resourceType",
            "code",
            "subject",
            "performedDateTime",
            "status",
        )
        model = UKCoreProcedure
