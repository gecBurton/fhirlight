
from api.models import Patient
from api.models.datatypes import Concept
from api.models.procedure import Procedure
from api.serializers.common import (
    UKCoreProfileSerializer,
    RelatedResourceSerializer,
    CodingSerializer,
)


class ProcedureSerializer(UKCoreProfileSerializer):
    code = CodingSerializer(valueset=Concept.VALUESET.UK_CORE_PROCEDURE_CODE)
    subject = RelatedResourceSerializer(queryset=Patient.objects.all())

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
