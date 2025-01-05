from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept


class EpisodeOfCareProfile(BaseProfile):
    """This profile allows exchange of information about an association between a patient and an organisation /
    healthcare providers during which time encounters may occur. The managing organisation assumes a level of
    responsibility for the individual during this time.

    Relationship to Encounter
    The EpisodeOfCare Resource contains information about an association of a Patient with a Healthcare Provider for a period of time under which related healthcare activities may occur. In many cases, this represents a period of time where the Healthcare Provider has some level of responsibility for the care of the patient regarding a specific condition or problem, even if not currently participating in an encounter. These resources are typically known in existing systems as:

    * EpisodeOfCare: Case, Program, Problem, Episode
    * Encounter: Visit, Contact.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-EpisodeOfCare
    # Current Version	2.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource EpisodeOfCare.

    class STATUS(models.TextChoices):
        PLANNED = "planned"
        WAIT_LIST = "waitlist"
        ACTIVE = "active"
        ON_HOLD = "onhold"
        FINISHED = "finished"
        CANCELLED = "cancelled"
        ENTERED_IN_ERROR = "entered-in-error"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="The status of the episode of care.",
    )

    type = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.EPISODE_OF_CARE_TYPE},
        blank=True,
        help_text="Type/class - e.g. specialist referral, disease management.",
        related_name="EpisodeOfCare_type",
    )

    patient = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="The patient who is the focus of this episode of care..",
        related_name="EpisodeOfCare_patient",
    )

    careManager = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        help_text="The practitioner that is the care manager/care coordinator for this patient.",
        related_name="EpisodeOfCare_careManager",
    )

    managingOrganization = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        on_delete=models.CASCADE,
        help_text="Organization that assumes care.",
        related_name="EpisodeOfCare_managingOrganization",
    )
