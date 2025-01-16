from django.db import models

from api.models.datatypes import (
    Name,
    Identifier,
    ContactPoint,
    Address,
    Concept,
    Extension,
)
from api.models.common import BaseProfile


class PatientProfile(BaseProfile):
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
    _birthDate = models.DateTimeField(null=True, blank=True, help_text="")


class PatientExtension(Extension):
    profile = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
    )

    class URL(models.TextChoices):
        ETHNIC_CATEGORY = "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-EthnicCategory"  # valueCodeableConcept
        CONTACT_PREFERENCE = "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-ContactPreference"  # extension
        PREFERRED_CONTACT_METHOD = "PreferredContactMethod"  # valueCodeableConcept
        PREFERRED_CONTACT_TIMES = "PreferredContactTimes"  # valueTiming
        PREFERRED_WRITTEN_COMMUNICATION_FORMAT = (
            "PreferredWrittenCommunicationFormat"  # valueCodeableConcept
        )
        DEATH_NOTIFICATION_STATUS = "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-DeathNotificationStatus"  # extension
        deathNotificationStatus = "deathNotificationStatus"  # valueCodeableConcept
        system_EFFECTIVE_DATE = "systemEffectiveDate"  # valueDateTime
        RESIDENTIAL_STATUS = "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-ResidentialStatus"  # valueCodeableConcept

    url = models.CharField(max_length=256)


class PatientIdentifier(Identifier):
    """An identifier for this patient."""

    class SYSTEM(models.TextChoices):
        NHS_NUMBER = "https://fhir.nhs.uk/Id/nhs-number"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
    )


class PatientTelecom(ContactPoint):
    """An identifier for this patient."""

    profile = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)


class PatientName(Name):
    profile = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )


class PatientAddress(Address):
    profile = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        help_text="A name associated with the contact person.",
    )
