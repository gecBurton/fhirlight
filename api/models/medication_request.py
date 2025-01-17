from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, Dosage, DoseAndRate


class MedicationRequestProfile(BaseProfile):
    """An order or request for both supply of the medication and the instructions for administration of the medication
    to an individual.

    This profile covers inpatient medication orders as well as community orders (whether filled by the prescriber or by
    a pharmacy). It also includes orders for over-the-counter medications (e.g. Aspirin), total parenteral nutrition
    and diet/ vitamin supplements, and may be used to support the order of medication-related devices.

    It is not intended for use in prescribing particular diets, or for ordering non-medication-related items
    (eyeglasses, supplies, etc).
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-MedicationRequest
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource MedicationRequest.

    # MedicationRequest.identifier	Allow the resource to be referenced within/by other resources

    class STATUS(models.TextChoices):
        ACTIVE = "active"
        DRAFT = "draft"
        ENTERED_IN_ERROR = "entered-in-error"
        ON_HOLD = "on-hold"
        REVOKED = "cancelled"
        STOPPED = "stopped"
        COMPLETED = "completed"
        UNKNOWN = "unknown"

    class INTENT(models.TextChoices):
        PROPOSAL = "proposal"
        PLAN = "plan"
        ORDER = "order"
        ORIGINAL_ORDER = "original-order"
        REFLEX_ORDER = "reflex-order"
        FILLER_ORDER = "filler-order"
        INTENT_ORDER = "instance-order"
        OPTION = "option"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="A code specifying the current state of the order.",
    )

    intent = models.CharField(
        max_length=16,
        choices=INTENT,
        help_text="Whether the request is a proposal, plan, or an original order.",
    )

    category = models.ManyToManyField(
        Concept,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_MEDICATION_REQUEST_CATEGORY_CODE
        },
        help_text="Provides the business context for the relevant dispensing processes",
        related_name="MedicationRequest_category",
    )
    courseOfTherapyType = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_MEDICATION_REQUEST_CATEGORY_CODE
        },
        help_text="A course of therapy for a medication request",
        related_name="MedicationRequest_courseOfTherapyType",
    )
    authoredOn = models.DateTimeField(
        null=True, blank=True, help_text="To timestamp the event"
    )

    medicationReference = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["medicationprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Identifies the medication being requested.",
        related_name="MedicationRequest_medicationReference",
    )
    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Who or group medication request is for",
        related_name="MedicationRequest_subject",
    )
    requester = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Who is requesting the medication",
        related_name="MedicationRequest_requester",
    )

    substitutionAllowedBoolean = models.BooleanField(
        null=True, blank=True, help_text="Any restrictions on medication substitution."
    )


class MedicationRequestDosageInstruction(Dosage):
    """Dosage instructions for the medication"""

    profile = models.ForeignKey(MedicationRequestProfile, on_delete=models.CASCADE)


class MedicationRequestDosageInstructionDoseAndRate(DoseAndRate):
    profile = models.ForeignKey(
        MedicationRequestDosageInstruction, on_delete=models.CASCADE
    )
