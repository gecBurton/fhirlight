from django.db import models

from api.fields import QuantityField
from api.models.common import BaseProfile
from api.models.datatypes import Concept, Identifier


class MedicationAdministrationProfile(BaseProfile):
    """The purpose of this profile is to describe the event of a patient consuming or otherwise being administered a
    medication. This may be as simple as swallowing a tablet, or it may be a long-running infusion.

    Related resources tie this event to the authorizing prescription, and the specific encounter between patient and
    health care practitioner."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-MedicationAdministration
    # Current Version	2.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource MedicationAdministration.

    class STATUS(models.TextChoices):
        IN_PROGRESS = "in-progress"
        NOT_DONE = "not-done"
        ON_HOLD = "on-hold"
        COMPLETED = "completed"
        ENTERED_IN_ERROR = "entered-in-error"
        STOPPED = "stopped"
        UNKNOWN = "unknown"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="Will generally be set to show that the administration has been completed. For some long running administrations such as infusions, it is possible for an administration to be started but not completed or it may be paused while some other process is under way.",
    )

    medicationReference = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["medicationprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Identifies the medication being requested.",
        related_name="MedicationAdministration_medicationReference",
    )
    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Who or group medication request is for",
        related_name="MedicationAdministration_subject",
    )
    request = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["medicationrequestprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Who is requesting the medication",
        related_name="MedicationAdministration_request",
    )

    effectiveDateTime = models.DateTimeField(
        null=True, blank=True, help_text="Start and end time of administration"
    )

    dosageText = models.TextField(
        null=True, blank=True, help_text="Free text dosage instructions."
    )

    dosageSite = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_BODY_SITE},
        help_text="Body site to administer to",
        related_name="MedicationAdministrationDosage_site",
    )

    dosageRoute = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_SUBSTANCE_OR_PRODUCT_ADMINISTRATION_ROUTE
        },
        help_text="How drug should enter body",
        related_name="MedicationAdministrationDosage_route",
    )

    dosageMethod = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_MEDICATION_DOSAGE_METHOD
        },
        help_text="Technique for administering medication",
        related_name="MedicationAdministrationDosage_method",
    )

    dosageRateQuantity = QuantityField(
        null=True, blank=True, help_text="Numerical value (with implicit precision)"
    )

    dosageDose = QuantityField(
        max_length=32, null=True, blank=True, help_text="Coded form of the unit"
    )


class MedicationAdministrationIdentifier(Identifier):
    """The address of the organisation using the Address datatype."""

    class SYSTEM(models.TextChoices):
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.ForeignKey(
        MedicationAdministrationProfile,
        on_delete=models.CASCADE,
    )
