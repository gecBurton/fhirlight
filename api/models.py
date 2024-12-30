from django.db import models
from api.datatypes import ContactPoint, Address, Identifier


class UKCore(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.CharField(primary_key=True, editable=False, unique=True, max_length=256)
    active = models.BooleanField(
        default=True, help_text="Whether the record is still in active use"
    )

    class Meta:
        abstract = True


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
        # limit_choices_to=[
        #     Identifier.SYSTEM.ODS_SITE_CODE,
        #     Identifier.SYSTEM.ODS_ORGANISATION_CODE,
        # ],
    )


# class Patient(UKCore):
#     """This profile allows exchange of demographics and other administrative information about an individual receiving
#     care or other health-related services.
#     """
#     # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Patient
#     # Current Version	2.4.0
#     # Last Updated	2023-04-28
#     # Description	This profile defines the UK constraints and extensions on the International FHIR resource Patient.
#
#
#     # Patient.telecom	A contact detail for the individual
#     # Patient.telecom.system	Telecommunications form for contact point
#     # Patient.telecom.value	The actual contact point details
#
#     # Patient.gender	the gender that the patient is considered to have for administration and record keeping purposes.
#     # Patient.birthDate	The date of birth for the individual.
#     # Patient.address	An address for the individual
#     # Patient.address.line	Street name, number, direction & P.O. Box etc.
#     # Patient.address.city	Name of city, town etc.
#     # Patient.address.postalCode	Postal code for area
#
#
# class PatientIdentifier(Identifier):
#     """An identifier for this patient."""
#
#     patient = models.ForeignKey(
#         Identifier,
#         on_delete=models.CASCADE,
#         limit_choices_to=[
#             Identifier.SYSTEM.ODS_SITE_CODE,
#             Identifier.SYSTEM.ODS_ORGANISATION_CODE,
#         ],
#     )
#
# class PatientName(Name):
#     patient = models.OneToOneField(Patient, on_delete=models.CASCADE, help_text="A name associated with the contact person.")
