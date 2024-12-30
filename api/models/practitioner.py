from django.db import models
from api.models.datatypes import ContactPoint, Address, Identifier, Name
from api.models.common import UKCore


class Practitioner(UKCore):
    """This profile allows exchange of information about all individuals who are engaged in the healthcare process and
    healthcare-related services as part of their formal responsibilities, is used for attribution of activities and
    responsibilities to these individuals.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Practitioner
    # Current Version	2.3.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Practitioner

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


class PractitionerAddress(Address):
    """The address of the practitioner using the Address datatype."""

    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)


class PractitionerIdentifier(Identifier):
    """An identifier that applies to this person in this role."""

    practitioner = models.ForeignKey(
        Practitioner,
        on_delete=models.CASCADE,
        limit_choices_to={
            "system": [
                Identifier.SYSTEM.GENERAL_MEDICAL_COUNCIL_REGISTRATION_NUMBER,
                Identifier.SYSTEM.GENERAL_PHARMACEUTICAL_COUNCIL_REGISTRATION_NUMBER,
                Identifier.SYSTEM.HEALTHCARE_PROFESSIONS_REGISTRATION_NUMBER,
                Identifier.SYSTEM.NURSES_MIDWIVES_HEALTH_VISITORS_COUNCIL_REGISTRATION_NUMBER,
                Identifier.SYSTEM.SPINE,
            ]
        },
    )


class PractitionerName(Name):
    """The name(s) associated with the practitioner."""

    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)


class PractitionerTelecom(ContactPoint):
    """A contact detail for the practitioner, e.g. a telephone number or an email address."""

    practitioner = models.ForeignKey(Practitioner, on_delete=models.CASCADE)
