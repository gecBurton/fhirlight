from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import (
    DataTypeWithPeriod,
    Identifier,
    Dosage,
    DoseAndRate,
)


class MedicationDispenseProfile(BaseProfile):
    """This profile covers the supply of medications to a patient. Examples include dispensing and pick-up from an
    outpatient or community pharmacy, dispensing patient-specific medications from inpatient pharmacy to ward, as well
    as issuing a single dose from ward stock to a patient for consumption. The medication dispense is the result of a
    pharmacy system responding to a medication order.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-MedicationDispense
    # Current Version	2.3.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource MedicationDispense.

    class STATUS(models.TextChoices):
        PREPARATION = "preparation"
        IN_PROGRESS = "in-progress"
        CANCELLED = "cancelled"
        ON_HOLD = "on-hold"
        COMPLETED = "completed"
        ENTERED_IN_ERROR = "entered-in-error"
        STOPPED = "stopped"
        DECLINED = "declined"
        UNKNOWN = "unknown"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="A code specifying the state of the set of dispense events.",
    )

    medicationReference = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["medicationprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Identifies the medication being requested.",
        related_name="MedicationDispense_medicationReference",
    )
    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Who or group medication request is for",
        related_name="MedicationDispense_subject",
    )
    authorizingPrescription = models.ManyToManyField(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["medicationrequestprofile"]},
        blank=True,
        help_text="Who is requesting the medication",
        related_name="MedicationDispense_authorizingPrescription",
    )
    receiver = models.ManyToManyField(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        blank=True,
        help_text="Who is requesting the medication",
        related_name="MedicationDispense_receiver",
    )

    whenPrepared = models.DateTimeField(
        null=True, blank=True, help_text="Start and end time of administration"
    )

    quantityValue = models.PositiveIntegerField(
        null=True, blank=True, help_text="Numerical value (with implicit precision)"
    )
    quantityUnit = models.CharField(
        max_length=32, null=True, blank=True, help_text="Unit representation"
    )
    quantitySystem = models.URLField(
        null=True, blank=True, help_text="System that defines coded unit form"
    )
    quantityCode = models.CharField(
        max_length=32, null=True, blank=True, help_text="Coded form of the unit"
    )

    daysSupplyValue = models.PositiveIntegerField(
        null=True, blank=True, help_text="Numerical value (with implicit precision)"
    )
    daysSupplyUnit = models.CharField(
        max_length=32, null=True, blank=True, help_text="Unit representation"
    )
    daysSupplySystem = models.URLField(
        null=True, blank=True, help_text="System that defines coded unit form"
    )
    daysSupplyCode = models.CharField(
        max_length=32, null=True, blank=True, help_text="Coded form of the unit"
    )

    # {
    #     "performer":  [
    #         {
    #             "actor": {
    #                 "reference": "Practitioner/UKCore-Practitioner-PharmacistJimmyChuck-Example"
    #             }
    #         }
    #     ],


class MedicationDispenseDosageInstruction(Dosage):
    """Dosage instructions for the medication"""

    profile = models.ForeignKey(MedicationDispenseProfile, on_delete=models.CASCADE)


class MedicationDispenseDosageInstructionDoseAndRate(DoseAndRate):
    dosageInstruction = models.ForeignKey(
        MedicationDispenseDosageInstruction, on_delete=models.CASCADE
    )


class MedicationDispenseIdentifier(Identifier):
    class SYSTEM(models.TextChoices):
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    profile = models.ForeignKey(MedicationDispenseProfile, on_delete=models.CASCADE)


class MedicationDispensePerformer(DataTypeWithPeriod):
    profile = models.ForeignKey(MedicationDispenseProfile, on_delete=models.CASCADE)
    actor = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Intended performer of administration",
        related_name="MedicationDispensePerformer_actor",
    )
