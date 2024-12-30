from django.db import models

from api.models.datatypes import Name, Identifier, ContactPoint, Address, Concept
from api.models.common import UKCore


class Patient(UKCore):
    """This profile allows exchange of demographics and other administrative information about an individual receiving
    care or other health-related services.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Patient
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Patient.

    # Patient.telecom	A contact detail for the individual
    # Patient.telecom.system	Telecommunications form for contact point
    # Patient.telecom.value	The actual contact point details

    # Patient.gender	the gender that the patient is considered to have for administration and record keeping purposes.
    # Patient.birthDate	The date of birth for the individual.
    # Patient.address	An address for the individual
    # Patient.address.line	Street name, number, direction & P.O. Box etc.
    # Patient.address.city	Name of city, town etc.
    # Patient.address.postalCode	Postal code for area

    class Gender(models.TextChoices):
        MALE = "male"
        FEMALE = "female"
        OTHER = "other"
        UNKNOWN = "unknown"

    gender = models.CharField(
        null=True,
        blank=True,
        max_length=8,
        choices=Gender,
        help_text="Administrative Gender - the gender that the person is considered to have for administration and record keeping purposes.",
    )
    birthDate = models.DateField(
        null=True, blank=True, help_text="The date of birth for the individual."
    )
    communication = models.ManyToManyField(
        Concept, limit_choices_to={"system": Concept.SYSTEM.LANGUAGE}, help_text=""
    )


class PatientIdentifier(Identifier):
    """An identifier for this patient."""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        limit_choices_to=[
            Identifier.SYSTEM.NHS_NUMBER,
        ],
    )


class PatientTelecom(ContactPoint):
    """An identifier for this patient."""

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class PatientName(Name):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )


class PatientAddress(Address):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )
