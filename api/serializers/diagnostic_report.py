from api.models.diagnostic_report import DiagnosticReport, DiagnosticReportIdentifier
from api.serializers.common import (
    UKCoreProfileSerializer,
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
