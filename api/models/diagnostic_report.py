from api.models import Patient, Observation, Organization, Specimen
from api.models.common import UKCore
from django.db import models

from api.models.datatypes import Concept, Identifier


class DiagnosticReport(UKCore):
    """This profile allows exchange of the findings and interpretation of diagnostic tests performed on individuals,
    groups of individuals, devices and locations and/or specimens derived from these. The report includes clinical
    context such as requesting and provider information and some mix of atomic results, images, textual and coded
    interpretations and formatted representation of diagnostic reports.

    Note: this profile SHALL NOT be used where a more specific UK Core profile exists.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-DiagnosticReport
    # Current Version	2.3.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource DiagnosticReport.

    class STATUS(models.TextChoices):
        registered = "registered"
        partial = "partial"
        preliminary = "preliminary"
        final = "final"

    status = models.CharField(
        max_length=16, choices=STATUS, help_text="The status of the diagnostic report."
    )
    category = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.DIAGNOSTIC_SERVICE_SECTION_CODE},
        help_text="A code that classifies the clinical discipline, department or diagnostic service that created the report.",
        related_name="diagnosticreportcategory_set",
    )
    code = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_REPORT_CODE},
        help_text="A code or name that describes this diagnostic report.",
    )
    subject = models.ForeignKey(
        Patient,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The subject of the report - usually, but not always, the patient",
    )

    # DiagnosticReport.encounter	Health care event when test ordered.
    effectiveDateTime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Clinically relevant time/time-period for report.",
    )
    result = models.ManyToManyField(
        Observation, help_text="that are part of this diagnostic report."
    )
    performer = models.ManyToManyField(
        Organization,
        help_text="Who is responsible for the observation",
    )
    specimen = models.ManyToManyField(
        Specimen,
        blank=True,
        help_text="Who is responsible for the observation",
    )


class DiagnosticReportIdentifier(Identifier):
    """An identifier for this patient."""

    class SYSTEM(models.TextChoices):
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    diagnostic_report = models.ForeignKey(
        DiagnosticReport,
        on_delete=models.CASCADE,
    )
