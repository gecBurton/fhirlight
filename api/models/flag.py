from django.db import models

from api.fields import PeriodField
from api.models.common import BaseProfile
from api.models.datatypes import Concept, Identifier


class FlagProfile(BaseProfile):
    """A flag is a warning or notification of some sort presented to the user - who may be a clinician or some other
    person involve in patient care. It usually represents something of sufficient significance to warrant a special
    display of some sort - rather than just a note in the resource. A flag has a subject representing the resource that
    will trigger its display.

    This subject can be of different types, as described in the examples below:

    * A note that a patient has an overdue account, which the provider may wish to discuss with them - in case of
      hardship, for example (subject = Patient)
    * An outbreak of Ebola in a particular region (subject = Location) so that all patients from that region have a
      higher risk of having that condition
    * A particular provider is unavailable for referrals over a given period (subject = Practitioner)
    * A patient who is enrolled in a clinical trial (subject = Group)
    * Special guidance or caveats to be aware of when following a protocol (subject = PlanDefinition)
    * Warnings about using a drug in a formulary requires special approval (subject = Medication)

    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Flag
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Flag

    class STATUS(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"
        ENTERED_IN_ERROR = "entered-in-error"

    status = models.CharField(
        max_length=16, choices=STATUS, help_text="Supports basic workflow."
    )

    code = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.FLAG_CODE},
        on_delete=models.CASCADE,
        help_text="The coded value or textual component of the flag to display to the user.",
        related_name="Flag_code",
    )

    category = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.FLAG_CATEGORY},
        blank=True,
        help_text="Clinical, administrative, etc.",
        related_name="Flag_v",
    )

    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The patient, location, group, organization, or practitioner etc. this is about record this flag is associated with.",
        related_name="Flag_subject",
    )
    encounter = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Alert relevant during encounter",
        related_name="Flag_encounter",
    )
    author = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Flag creator",
        related_name="Flag_author",
    )
    period = PeriodField(
        null=True,
        blank=True,
        help_text="Start time period when the record was/is in use",
    )


class FlagIdentifier(Identifier):
    """An identifier for this device."""

    system = models.URLField(
        max_length=64,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.ForeignKey(
        FlagProfile,
        on_delete=models.CASCADE,
    )
