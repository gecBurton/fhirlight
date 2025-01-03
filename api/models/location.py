from django.db import models

from api.models import UKCoreOrganization
from api.models.common import UKCore
from api.models.datatypes import Address, Identifier, ContactPoint, Concept


class LocationAddress(Address):
    pass


class UKCoreLocation(UKCore):
    """This profile can be used to exchange details and position information for a physical place where services are
    provided and resources and participants may be stored, found, contained, or accommodated.

    A location includes both incidental locations (a place which is used for healthcare without prior designation or
    authorisation) and dedicated, formally appointed locations. Locations may be private, public, mobile or fixed and
    scale from small freezers to full hospital buildings or parking garages.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Location
    # Current Version	2.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Location.

    # Location.identifier:odsSiteCode	ODS Site code to identify the organisation at site level.

    class STATUS(models.TextChoices):
        ACTIVE = "active"
        SUSPENDED = "suspended"
        INACTIVE = "inactive"

    status = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=STATUS,
        help_text="Is the location active, inactive, or suspended.",
    )
    name = models.TextField(
        null=True,
        blank=True,
        help_text="Name of the location as used by humans. This does not need to be unique.",
    )
    managingOrganization = models.ForeignKey(
        UKCoreOrganization,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Organization responsible for provisioning and upkeep",
    )
    type = models.ManyToManyField(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.SERVICE_DELIVERY_LOCATION_ROLE_TYPE
        },
        help_text="Type of function performed",
    )

    address = models.OneToOneField(
        LocationAddress,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="If locations can be visited, we need to keep track of their address.",
    )


class LocationIdentifier(Identifier):
    class SYSTEM(models.TextChoices):
        ODS_SITE_CODE = "https://fhir.nhs.uk/Id/ods-site-code"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    location = models.ForeignKey(
        UKCoreLocation,
        on_delete=models.CASCADE,
    )


class LocationTelecom(ContactPoint):
    location = models.ForeignKey(
        UKCoreLocation,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )
