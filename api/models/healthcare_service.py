from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.fields import PeriodField
from api.models.common import BaseProfile
from api.models.datatypes import Concept, ContactPoint, DataTypeWithPeriod, Identifier


class HealthcareServiceProfile(BaseProfile):
    """This profile is used to describe a single healthcare service or category of services that are provided by an
    organisation at a location, including a virtual location.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-HealthcareService
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource HealthcareService.

    providedBy = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Organization that provides this service",
        related_name="HealthcareService_providedBy",
    )

    location = models.ManyToManyField(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["locationprofile"]},
        blank=True,
        help_text="Location(s) where service may be provided",
        related_name="HealthcareService_location",
    )

    category = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_CATEGORY},
        blank=True,
        help_text="Broad category of service being performed or delivered",
        related_name="HealthcareService_category",
    )
    type = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_TYPE},
        blank=True,
        help_text="Type of service that may be delivered or performed",
        related_name="HealthcareService_type",
    )
    specialty = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE},
        blank=True,
        help_text="Specialties handled by the HealthcareService.",
        related_name="HealthcareService_specialty",
    )
    serviceProvisionCode = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SERVICE_PROVISION_CONDITIONS},
        blank=True,
        help_text="Conditions under which service is available/offered",
        related_name="HealthcareService_serviceProvisionCode",
    )
    characteristic = models.ManyToManyField(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.HEALTHCARE_SERVICE_CHARACTERISTIC
        },
        blank=True,
        help_text="Collection of characteristics (attributes)",
        related_name="HealthcareService_characteristic",
    )
    referralMethod = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.REFERRAL_METHOD},
        blank=True,
        help_text="Ways that the service accepts referrals",
        related_name="HealthcareService_referralMethod",
    )

    name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="Description of service as presented to a consumer while searching",
    )
    comment = models.TextField(
        null=True,
        blank=True,
        help_text="Additional description and/or any specific issues not covered elsewhere",
    )
    extraDetails = models.TextField(
        null=True,
        blank=True,
        help_text="Extra details about the service that can't be placed in the other fields",
    )
    appointmentRequired = models.BooleanField(
        null=True,
        blank=True,
        help_text="If an appointment is required for access to this service",
    )
    availabilityExceptions = models.TextField(
        null=True, blank=True, help_text="Description of availability exceptions"
    )


class HealthcareServiceTelecom(ContactPoint):
    profile = models.ForeignKey(
        HealthcareServiceProfile,
        on_delete=models.CASCADE,
    )


class HealthcareServiceIdentifier(Identifier):
    profile = models.ForeignKey(
        HealthcareServiceProfile,
        on_delete=models.CASCADE,
    )
    system = models.CharField(max_length=128, null=True, blank=True)


class HealthcareServiceAvailableTime(DataTypeWithPeriod):
    profile = models.ForeignKey(
        HealthcareServiceProfile,
        on_delete=models.CASCADE,
    )

    class DaysOfTheWeek(models.TextChoices):
        MON = "mon", "Monday"
        TUESDAY = "tue", "Tuesday"
        WEDNESDAY = "wed", "Wednesday"
        THURSDAY = "thu", "Thursday"
        FRIDAY = "fri", "Friday"
        SATURDAY = "sat", "Saturday"
        SUNDAY = "sun", "Sunday"

    daysOfWeek = ArrayField(
        models.CharField(max_length=3, choices=DaysOfTheWeek),
        null=True,
        blank=True,
        help_text="Indicates which days of the week are available between the start and end Times.",
    )
    allDay = models.BooleanField(
        null=True, blank=True, help_text="Always available? e.g. 24 hour service"
    )
    availableStartTime = models.TimeField(
        null=True,
        blank=True,
        help_text="Opening time of day (ignored if allDay = true)",
    )
    availableEndTime = models.TimeField(
        null=True,
        blank=True,
        help_text="Closing time of day (ignored if allDay = true)",
    )


class HealthcareServiceNotAvailable(DataTypeWithPeriod):
    profile = models.ForeignKey(
        HealthcareServiceProfile,
        on_delete=models.CASCADE,
    )
    description = models.CharField(
        max_length=128, help_text="Times the Service Site is available"
    )
    during = PeriodField(
        null=True, blank=True, help_text="Service not available from this date"
    )

    #     "program":  [
    #         {
    #             "text": "Leeds Orthopaedic Outreach Service"
    #         }
    #     ],
    # }
