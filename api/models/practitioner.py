from django.db import models

from api.fields import PeriodField
from api.models import OrganizationProfile
from api.models.datatypes import (
    ContactPoint,
    Address,
    Identifier,
    Name,
    DataTypeWithPeriod,
    Concept,
)
from api.models.common import BaseProfile


class PractitionerProfile(BaseProfile):
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

    birthDate = models.DateField(
        null=True, blank=True, help_text="The date on which the practitioner was born"
    )
    communication = models.ManyToManyField(
        Concept,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_HUMAN_LANGUAGE},
        help_text="A language the practitioner can use in patient communication",
    )


class PractitionerQualification(DataTypeWithPeriod):
    """The official certifications, training, and licenses that authorize or otherwise pertain to the provision of care
    by the practitioner. For example, a medical license issued by a medical board authorizing the practitioner to
    practice medicine within a certain locality.
    """

    profile = models.ForeignKey(PractitionerProfile, on_delete=models.CASCADE)
    code = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.DEGREE_LICENSE_CERTIFICATE},
        help_text="Coded representation of the qualification.",
    )
    period = PeriodField(
        null=True,
        blank=True,
        help_text="Period during which the qualification is valid.",
    )
    issuer = models.ForeignKey(
        OrganizationProfile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Organization that regulates and issues the qualification.",
    )


class PractitionerQualificationIdentifier(Identifier):
    """An identifier that applies to this person's qualification in this role"""

    system = models.URLField(
        max_length=64,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    practitioner_qualification = models.ForeignKey(
        PractitionerQualification,
        on_delete=models.CASCADE,
    )


class PractitionerAddress(Address):
    """The address of the practitioner using the Address datatype."""

    profile = models.ForeignKey(PractitionerProfile, on_delete=models.CASCADE)


class PractitionerIdentifier(Identifier):
    """An identifier that applies to this person in this role."""

    class SYSTEM(models.TextChoices):
        NHS_NUMBER = "https://fhir.nhs.uk/Id/nhs-number"
        GENERAL_MEDICAL_COUNCIL_REGISTRATION_NUMBER = (
            "https://fhir.hl7.org.uk/Id/gmc-number"
        )
        GENERAL_PHARMACEUTICAL_COUNCIL_REGISTRATION_NUMBER = (
            "https://fhir.hl7.org.uk/Id/gphc-number"
        )
        NURSES_MIDWIVES_HEALTH_VISITORS_COUNCIL_REGISTRATION_NUMBER = (
            "https://fhir.hl7.org.uk/Id/nmc-number"
        )
        HEALTHCARE_PROFESSIONS_REGISTRATION_NUMBER = (
            "https://fhir.hl7.org.uk/Id/hcpc-number"
        )
        SPINE = "https://fhir.nhs.uk/Id/sds-user-id"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.ForeignKey(
        PractitionerProfile,
        on_delete=models.CASCADE,
    )


class PractitionerName(Name):
    """The name(s) associated with the practitioner."""

    profile = models.ForeignKey(PractitionerProfile, on_delete=models.CASCADE)


class PractitionerTelecom(ContactPoint):
    """A contact detail for the practitioner, e.g. a telephone number or an email address."""

    profile = models.ForeignKey(PractitionerProfile, on_delete=models.CASCADE)
