from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, DataTypeWithPeriod


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


class MedicationRequestDosageInstruction(DataTypeWithPeriod):
    """Dosage instructions for the medication"""

    profile = models.ForeignKey(MedicationRequestProfile, on_delete=models.CASCADE)

    class UCUM(models.TextChoices):
        """unit of time"""

        SECOND = "s"
        MINUTE = "min"
        HOUR = "h"
        DAY = "d"
        WEEK = "wk"
        MONTH = "mo"
        ANNUAL = "a"

    # dispenseRequest	Specific dispensing quantity instructions.
    dispenseRequestQuantityValue = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Amount of medication to supply per dispense. Numerical value (with implicit precision)",
    )
    dispenseRequestQuantityUnit = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text="Amount of medication to supply per dispense. Unit representation",
    )
    dispenseRequestQuantitySystem = models.URLField(
        null=True,
        blank=True,
        help_text="Amount of medication to supply per dispense. System that defines coded unit form",
    )
    dispenseRequestQuantityCode = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Amount of medication to supply per dispense. Coded form of the unit",
    )

    text = models.TextField(
        null=True, blank=True, help_text="Free text dosage instructions."
    )

    site = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_BODY_SITE},
        help_text="Body site to administer to",
        related_name="MedicationRequestDosageInstruction_site",
    )
    route = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_SUBSTANCE_OR_PRODUCT_ADMINISTRATION_ROUTE
        },
        help_text="How drug should enter body",
        related_name="MedicationRequestDosageInstruction_route",
    )
    method = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_MEDICATION_DOSAGE_METHOD
        },
        help_text="Technique for administering medication",
        related_name="MedicationRequestDosageInstruction_method",
    )

    timingRepeatFrequency = models.PositiveIntegerField(
        null=True, blank=True, help_text="Event occurs frequency times per period"
    )
    timingRepeatPeriod = models.FloatField(
        null=True, blank=True, help_text="Event occurs frequency times per period"
    )
    timingRepeatPeriodUnit = models.CharField(
        choices=UCUM,
        max_length=8,
        null=True,
        blank=True,
        help_text="The units of time for the period in UCUM units.",
    )


class MedicationRequestDosageInstructionDoseAndRate(DataTypeWithPeriod):
    dosageInstruction = models.ForeignKey(
        MedicationRequestDosageInstruction, on_delete=models.CASCADE
    )

    type = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.DOSE_AND_RATE_TYPE_CODE},
        help_text="The kind of dose or rate specified",
        related_name="MedicationRequestDosageInstructionDoseAndRate_type",
    )
    doseQuantityValue = models.PositiveIntegerField(
        null=True, blank=True, help_text="Numerical value (with implicit precision)"
    )
    doseQuantityUnit = models.CharField(
        max_length=16, null=True, blank=True, help_text="Unit representation"
    )
    doseQuantitySystem = models.URLField(
        null=True, blank=True, help_text="System that defines coded unit form"
    )
    doseQuantityCode = models.CharField(
        max_length=32, null=True, blank=True, help_text="Coded form of the unit"
    )


#     "substitution": {
#         "allowedBoolean": true
#     }
