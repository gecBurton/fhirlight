from django.db import models

from api.models import UKCorePractitioner, UKCoreOrganization, UKCoreLocation
from api.models.common import UKCore
from api.models.datatypes import ContactPoint, Concept, Identifier


class UKCorePractitionerRole(UKCore):
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
        related_name="practitionerrole_code",
    )
    practitioner = models.ForeignKey(
        UKCorePractitioner,
        on_delete=models.CASCADE,
        help_text="Practitioner that is able to provide the defined services for the organization.",
    )
    organization = models.ForeignKey(
        UKCoreOrganization,
        on_delete=models.CASCADE,
        help_text="Organization where the roles are available.",
    )
    location = models.ManyToManyField(
        UKCoreLocation,
        help_text="The location(s) at which this practitioner provides care",
    )

    period_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Start time period when the resource was/is in use",
    )
    period_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text="End time period when the resource was/is in use",
    )
    specialty = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE},
        help_text="Specific specialty of the practitioner",
    )


class PractitionerRoleTelecom(ContactPoint):
    """Contact details that are specific to the role/location/service"""

    practitioner_role = models.ForeignKey(
        UKCorePractitionerRole, on_delete=models.CASCADE
    )


class PractitionerRoleIdentifier(Identifier):
    class SYSTEM(models.TextChoices):
        SDS_ROLE_PROFILE_ID = "https://fhir.nhs.uk/Id/sds-role-profile-id"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    practitioner_role = models.ForeignKey(
        UKCorePractitionerRole, on_delete=models.CASCADE
    )
