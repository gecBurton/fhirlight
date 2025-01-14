from api.models.diagnostic_report import (
    DiagnosticReportProfile,
)
from api.serializers.common import (
    ProfileSerializer,
)


class DiagnosticReportSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = DiagnosticReportProfile
