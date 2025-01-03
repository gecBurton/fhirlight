from api.models.datatypes import Concept
from api.models.diagnostic_report import DiagnosticReport, DiagnosticReportIdentifier
from api.serializers.common import (
    UKCoreProfileSerializer,
    CodingSerializer,
    UKCoreModelSerializer,
)


class DiagnosticReportIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "diagnostic_report", "created_at", "updated_at")
        model = DiagnosticReportIdentifier


class DiagnosticReportSerializer(UKCoreProfileSerializer):
    identifier = DiagnosticReportIdentifierSerializer(
        many=True, required=False, source="diagnosticreportidentifier_set"
    )
    category = CodingSerializer(
        required=False,
        many=True,
        valueset=Concept.VALUESET.DIAGNOSTIC_SERVICE_SECTION_CODE,
    )
    code = CodingSerializer(valueset=Concept.VALUESET.UK_CORE_REPORT_CODE)

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "performer",
            "specimen",
            "status",
            "effectiveDateTime",
            "category",
            "code",
            "subject",
            "result",
        )
        model = DiagnosticReport
