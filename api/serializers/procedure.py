from api.models.datatypes import Concept
from api.models.procedure import Procedure
from api.serializers.common import (
    UKCoreProfileSerializer,
    CodingSerializer,
)


class ProcedureSerializer(UKCoreProfileSerializer):
    code = CodingSerializer(valueset=Concept.VALUESET.UK_CORE_PROCEDURE_CODE)

    class Meta:
        fields = (
            "id",
            "resourceType",
            "code",
            "subject",
            "performedDateTime",
            "status",
        )
        model = Procedure
