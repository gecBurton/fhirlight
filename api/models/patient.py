from django.db import models

from api.models.datatypes import Name, Identifier, ContactPoint, Address, Concept
from api.models.common import UKCore


class UKCorePatient(UKCore):
    """This profile allows exchange of demographics and other administrative information about an individual receiving
    care or other health-related services.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Patient
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Patient.

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
        Concept,
        limit_choices_to={"system": Concept.VALUESET.UK_CORE_HUMAN_LANGUAGE},
        help_text="",
    )


class PatientIdentifier(Identifier):
    """An identifier for this patient."""

    class SYSTEM(models.TextChoices):
        NHS_NUMBER = "https://fhir.nhs.uk/Id/nhs-number"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    patient = models.ForeignKey(
        UKCorePatient,
        on_delete=models.CASCADE,
    )


class PatientTelecom(ContactPoint):
    """An identifier for this patient."""

    patient = models.ForeignKey(UKCorePatient, on_delete=models.CASCADE)


class PatientName(Name):
    patient = models.ForeignKey(
        UKCorePatient,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )


class PatientAddress(Address):
    patient = models.ForeignKey(
        UKCorePatient,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )
