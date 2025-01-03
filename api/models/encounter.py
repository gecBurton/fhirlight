from django.db import models

from api.models import Patient, Practitioner, Organization, Location
from api.models.common import UKCore
from api.models.datatypes import Concept, Identifier


class Encounter(UKCore):
    """dance or caveats to be aware of when following a protocol (subject = PlanDefinition)
    * Warnings about using a drug in a formulary requires special approval (subject = Medication)
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Flag
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Flag.

    class STATUS(models.TextChoices):
        PLANNED = "planned"
        ARRIVED = "arrived"
        TRIAGED = "triaged"
        IN_PROGRESS = "in-progress"
        ON_LEAVE = "onleave"
        FINISHED = "finished"
        CANCELLED = "cancelled"

    status = models.CharField(
        max_length=16, choices=STATUS, help_text="Supports basic workflow."
    )
    klass = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.V3_ACT_ENCOUNTER_CODE},
        help_text="Classification of patient encounter",
        related_name="encounterclass_set",
    )
    type = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_ENCOUNTER_TYPE},
        help_text="Specific type of encounter",
        related_name="encountertype_set",
    )
    subject = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The patient or group present at the encounter",
    )
    periodStart = models.DateTimeField(
        null=True, blank=True, help_text="The start time of the encounter."
    )
    periodEnd = models.DateTimeField(
        null=True, blank=True, help_text="The end time of the encounter."
    )
    reasonCode = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.ENCOUNTER_REASON_CODE},
        help_text="Indication, Admission diagnosis",
        related_name="encounterreasoncode_set",
    )
    serviceProvider = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The organization (facility) responsible for this encounter",
    )


class EncounterHospitalization(models.Model):
    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
    )
    dischargeDisposition = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_DISCHARGE_DESTINATION},
        help_text="Category or kind of location after discharge",
    )


class EncounterParticipant(models.Model):
    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
    )
    individual = models.ForeignKey(
        Practitioner,
        on_delete=models.CASCADE,
    )
    type = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.PARTICIPANT_TYPE},
        related_name="encounterparticipanttype_set",
    )


class EncounterLocation(models.Model):
    """List of locations where the patient has been"""

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
    )


class EncounterIdentifier(Identifier):
    """An identifier for this patient."""

    class SYSTEM(models.TextChoices):
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
    )