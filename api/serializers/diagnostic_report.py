from api.models.diagnostic_report import (
    DiagnosticReportProfile,
    DiagnosticReportIdentifier,
)
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class DiagnosticReportIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "diagnostic_report", "created_at", "updated_at")
        model = DiagnosticReportIdentifier


class DiagnosticReportSerializer(ProfileSerializer):
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
        model = DiagnosticReportProfile
