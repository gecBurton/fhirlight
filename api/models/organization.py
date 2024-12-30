from django.db import models

from api.models.datatypes import Identifier, ContactPoint, Address
from api.models.common import UKCore


class Organization(UKCore):
    """This profile allows exchange of a formally or informally recognised grouping of people or organisations formed
    for the purpose of achieving some form of collective action. Includes companies, institutions, corporations,
    departments, community groups, healthcare practice groups, etc.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Organization
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Organization.

    name = models.TextField(help_text="A name associated with the organization.")


class OrganizationContactPoint(ContactPoint):
    """A contact detail (e.g. a telephone number or an email address) by which the organisation may be contacted."""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class OrganizationAddress(Address):
    """The address of the organisation using the Address datatype."""

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class OrganizationIdentifier(Identifier):
    """The address of the organisation using the Address datatype."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        limit_choices_to={
            "system": [
                Identifier.SYSTEM.ODS_SITE_CODE,
                Identifier.SYSTEM.ODS_ORGANISATION_CODE,
            ]
        },
    )
