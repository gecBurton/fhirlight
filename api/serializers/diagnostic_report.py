from api.models import Patient, Observation, Organization, Specimen

from api.models.datatypes import Concept
from api.models.diagnostic_report import DiagnosticReport, DiagnosticReportIdentifier
from api.serializers.common import (
    UKCoreProfileSerializer,
    CodingSerializer,
    RelatedResourceSerializer,
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
    subject = RelatedResourceSerializer(queryset=Patient.objects.all(), required=False)
    result = RelatedResourceSerializer(
        queryset=Observation.objects.all(), required=False, many=True
    )
    performer = RelatedResourceSerializer(
        required=False, many=True, queryset=Organization.objects.all()
    )
    specimen = RelatedResourceSerializer(
        required=False, many=True, queryset=Specimen.objects.all()
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
