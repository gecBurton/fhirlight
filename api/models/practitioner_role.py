from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import CharField

from api.fields import PeriodField
from api.models.common import BaseProfile
from api.models.datatypes import Concept, ContactPoint, DataTypeWithPeriod, Identifier


class PractitionerRoleProfile(BaseProfile):
    """This profile allows exchange of a specific set of roles, specialties and services that a practitioner may
    perform at an organisation for a period of time.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-PractitionerRole
    # Current Version	2.3.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource PractitionerRole.

    code = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.PRACTITIONER_ROLE},
        help_text="Roles which this practitioner may perform",
        related_name="PractitionerRole_code",
    )

    practitioner = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        help_text="Practitioner that is able to provide the defined services for the organization.",
        related_name="PractitionerRole_practitioner",
    )

    organization = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        on_delete=models.CASCADE,
        help_text="Organization where the roles are available.",
        related_name="PractitionerRole_organization",
    )

    location = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["locationprofile"]},
        help_text="The location(s) at which this practitioner provides care",
        related_name="PractitionerRole_location",
    )

    healthcareService = models.ManyToManyField(
        BaseProfile,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["healthcareserviceprofile"]},
        help_text="The list of healthcare services that this worker provides for this role's Organization/Location(s).",
        related_name="PractitionerRole_healthcareService",
    )

    period = PeriodField(
        null=True,
        blank=True,
        help_text="Start time period when the resource was/is in use",
    )

    specialty = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE},
        help_text="Specific specialty of the practitioner",
    )

    availabilityExceptions = models.TextField(
        null=True, blank=True, help_text="Description of availability exceptions"
    )


class PractitionerRoleTelecom(ContactPoint):
    """Contact details that are specific to the role/location/service"""

    profile = models.ForeignKey(PractitionerRoleProfile, on_delete=models.CASCADE)


class PractitionerRoleIdentifier(Identifier):
    class SYSTEM(models.TextChoices):
        SDS_ROLE_PROFILE_ID = "https://fhir.nhs.uk/Id/sds-role-profile-id"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    profile = models.ForeignKey(PractitionerRoleProfile, on_delete=models.CASCADE)


class PractitionerRoleAvailableTime(DataTypeWithPeriod):
    class DaysOfTheWeek(models.TextChoices):
        MON = "mon", "Monday"
        TUESDAY = "tue", "Tuesday"
        WEDNESDAY = "wed", "Wednesday"
        THURSDAY = "thu", "Thursday"
        FRIDAY = "fri", "Friday"
        SATURDAY = "sat", "Saturday"
        SUNDAY = "sun", "Sunday"

    profile = models.ForeignKey(PractitionerRoleProfile, on_delete=models.CASCADE)
    daysOfWeek = ArrayField(
        CharField(choices=DaysOfTheWeek, max_length=4),
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


class PractitionerRoleNotAvailable(DataTypeWithPeriod):
    profile = models.ForeignKey(PractitionerRoleProfile, on_delete=models.CASCADE)
    description = models.TextField(
        help_text="Reason presented to the user explaining why time not available"
    )
    during = PeriodField(
        null=True, blank=True, help_text="Service not available from this date"
    )
