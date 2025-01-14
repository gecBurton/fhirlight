from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.models.datatypes import Identifier, ContactPoint, Address, Concept
from api.models.common import BaseProfile


class OrganizationProfile(BaseProfile):
    """This profile allows exchange of a formally or informally recognised grouping of people or organisations formed
    for the purpose of achieving some form of collective action. Includes companies, institutions, corporations,
    departments, community groups, healthcare practice groups, etc.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Organization
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Organization.

    type = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_ORGANIZATION_TYPE},
        blank=True,
        help_text="The kind(s) of organization that this is.",
        related_name="Organization_type",
    )
    name = models.TextField(help_text="A name associated with the organization.")
    alias = ArrayField(
        models.CharField(max_length=256),
        null=True,
        blank=True,
        help_text="A list of alternate names that the organization is known as, or was known as in the past.",
    )
    partOf = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The organization of which this organization forms a part.",
        related_name="Organization_partOf",
    )


class OrganizationTelecom(ContactPoint):
    """A contact detail (e.g. a telephone number or an email address) by which the organisation may be contacted."""

    profile = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)


class OrganizationAddress(Address):
    """The address of the organisation using the Address datatype."""

    profile = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)


class OrganizationIdentifier(Identifier):
    """The address of the organisation using the Address datatype."""

    class SYSTEM(models.TextChoices):
        ODS_ORGANISATION_CODE = "https://fhir.nhs.uk/Id/ods-organization-code"
        ODS_SITE_CODE = "https://fhir.nhs.uk/Id/ods-site-code"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.ForeignKey(
        OrganizationProfile,
        on_delete=models.CASCADE,
    )
