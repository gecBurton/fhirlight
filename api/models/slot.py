from django.db import models

from api.models.common import UKCore
from api.models.datatypes import Concept, Identifier


class UKCoreSlot(UKCore):
    """Slot resources are used to provide time-slots that can be booked using an appointment. They do not provide any
    information about appointments that are available, just the time, and optionally what the time can be used for.
    These are effectively spaces of free/busy time. Slots can also be marked as busy without having appointments
    associated."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Slot
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Slot.

    class STATUS(models.TextChoices):
        BUSY = "busy"
        FREE = "free"
        BUSY_UNAVAILABLE = "busy-unavailable"
        BUSY_TENTATIVE = "busy-tentative"
        ENTERED_IN_ERROR = "entered-in-error"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="The status of the slot, e.g free, busy, etc.",
    )
    start = models.DateTimeField(help_text="Date/Time that the slot is to begin.")
    end = models.DateTimeField(help_text="Date/Time that the slot is to conclude.")

    serviceCategory = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_CATEGORY},
        help_text="A broad categorization of the service that is to be performed during this appointment.",
        related_name="slot_servicecategory",
    )
    serviceType = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_TYPE},
        help_text="The type of appointments that can be booked into this slot (ideally this would be an identifiable service - which is at a location, rather than the location itself). If provided then this overrides the value provided on the availability resource.",
        related_name="slot_servicetype",
    )
    specialty = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE},
        help_text="The specialty of a practitioner that would be required to perform the service requested in this appointment.",
        related_name="slot_speciality",
    )

    appointmentType = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.V2_0276},
        help_text="The style of appointment or patient that may be booked in the slot.",
        related_name="slot_appointmenttype",
    )
    comment = models.TextField(
        null=True,
        blank=True,
        help_text="Comments on the slot to describe any extended information. Such as custom constraints on the slot",
    )


class SlotIdentifier(Identifier):
    """External Ids for this item"""

    class SYSTEM(models.TextChoices):
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    slot = models.ForeignKey(
        UKCoreSlot,
        on_delete=models.CASCADE,
    )
