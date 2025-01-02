from django.db import models

from api.models import Location
from api.models.common import UKCore
from api.models.datatypes import Identifier, Concept


class Schedule(UKCore):
    """Schedule resources provide a container for time-slots that can be booked using an appointment. It provides the
    window of time (period) that slots are defined for and what type of appointments can be booked.

    The schedule does not provide any information about actual appointments. This separation greatly assists where
    access to the appointments would not be permitted for security or privacy reasons, while still being able to
    determine if an appointment might be available.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Schedule
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Schedule.

    comment = models.TextField(
        null=True, blank=True, help_text="Comments on availability"
    )
    serviceCategory = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_CATEGORY},
        help_text="High-level category.",
        related_name="schedule_servicecategory_set",
    )
    serviceType = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_TYPE},
        help_text="Specific service.",
        related_name="schedule_servicetype_set",
    )
    specialty = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE},
        help_text="Type of specialty needed.",
        related_name="schedule_specialty_set",
    )
    planningHorizonStart = models.DateTimeField(
        null=True, blank=True, help_text="Period of time covered by schedule."
    )
    planningHorizonEnd = models.DateTimeField(
        null=True, blank=True, help_text="Period of time covered by schedule."
    )
    actor = models.ManyToManyField(
        Location,
        help_text="Resource(s) that availability information is being provided for",
    )


class ScheduleIdentifier(Identifier):
    class SYSTEM(models.TextChoices):
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
