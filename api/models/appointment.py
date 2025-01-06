from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, Identifier, DataTypeWithPeriod


class AppointmentProfile(BaseProfile):
    """This profile allows recording of detailed information about a planned meeting that may be in the future or past.
    The resource only describes a single meeting, a series of repeating visits would require multiple appointment
    resources to be created for each instance.

    Examples include a scheduled surgery, a follow-up for a clinical visit, a scheduled conference call between
    clinicians to discuss a case, the reservation of a piece of diagnostic equipment for a particular use, etc. The
    visit scheduled by an appointment may be in person or remote (by phone, video conference, etc.) All that matters is
    that the time and usage of one or more individuals, locations and/or pieces of equipment is being fully or
    partially reserved for a designated period of time.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Appointment
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Appointment.

    class STATUS(models.TextChoices):
        PROPOSED = "proposed"
        PENDING = "pending"
        BOOKED = "booked"
        ARRIVED = "arrived"
        FULFILLED = "fulfilled"
        CANCELLED = "cancelled"
        NO_SHOW = "noshow"
        ENTERED_IN_ERROR = "entered-in-error"
        checked_IN = "checked-in"
        WAIT_LIST = "waitlist"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="The overall status of the Appointment.",
    )
    serviceCategory = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_CATEGORY},
        blank=True,
        help_text="A broad categorization of the service that is to be performed during this appointment.",
        related_name="AppointmentProfile_serviceCategory",
    )
    serviceType = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_TYPE},
        blank=True,
        help_text="The specific service that is to be performed during this appointment.",
        related_name="AppointmentProfile_serviceType",
    )
    specialty = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE},
        blank=True,
        help_text="The specialty of a practitioner that would be required to perform the service requested in this appointment.",
        related_name="AppointmentProfile_specialty",
    )
    appointmentType = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_APPOINTMENT_REASON_CODE},
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="The style of appointment or patient that has been booked in the slot (not service type).",
        related_name="AppointmentProfile_appointmentType",
    )
    priority = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Used to make informed decisions if needing to re-prioritize",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Shown on a subject line in a meeting request, or appointment list",
    )
    start = models.DateTimeField(
        null=True, blank=True, help_text="When appointment is to take place"
    )
    end = models.DateTimeField(
        null=True, blank=True, help_text="When appointment is to conclude"
    )
    created = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date that this appointment was initially created",
    )
    comment = models.TextField(null=True, blank=True, help_text="Additional comments")
    patientInstruction = models.TextField(
        null=True,
        blank=True,
        help_text="Detailed information and instructions for the patient",
    )
    reasonReference = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["conditionprofile"]},
        help_text="Reason the appointment is to take place (resource)",
        related_name="Appointment_reasonReference",
    )
    basedOn = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["servicerequestprofile"]},
        help_text="The service request this appointment is allocated to assess",
        related_name="Appointment_basedOn",
    )


class AppointmentIdentifier(Identifier):
    """External Ids for this item."""

    system = models.URLField(
        max_length=64,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    appointment = models.ForeignKey(
        AppointmentProfile,
        on_delete=models.CASCADE,
    )


class AppointmentParticipant(DataTypeWithPeriod):
    class REQUIRED(models.TextChoices):
        REQUIRED = "required"
        OPTIONAL = "optional"
        INFORMATION_ONLY = "information-only"

    class STATUS(models.TextChoices):
        ACCEPTED = "accepted"
        DECLINED = "declined"
        TENTATIVE = "tentative"
        NEEDS_ACTION = "needs-action"

    appointment = models.ForeignKey(
        AppointmentProfile,
        on_delete=models.CASCADE,
    )

    type = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE},
        blank=True,
        help_text="Role of participant in the appointment.",
        related_name="AppointmentParticipant_type",
    )
    actor = models.ForeignKey(
        BaseProfile,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        limit_choices_to={
            "polymorphic_ctype__model__in": [
                "practitionerprofile",
                "patientprofile",
                "locationprofile",
            ]
        },
        help_text="Person, Location/HealthcareService or Device",
        related_name="AppointmentParticipant_actor",
    )

    required = models.CharField(
        null=True,
        blank=True,
        choices=REQUIRED,
        max_length=16,
        help_text="Whether this participant is required to be present at the meeting.",
    )
    status = models.CharField(
        max_length=16, choices=STATUS, help_text="Participation status of the actor."
    )
