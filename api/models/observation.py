from django.db import models

from api.models import Organization, Patient
from api.models.common import UKCore
from api.models.datatypes import Concept, Identifier


class Observation(UKCore):
    """This profile allows exchange of information of Measurements and simple assertions made about an individual,
    device or other subject.
    Note: this profile SHALL NOT be used where a more specific UK Core profile exists."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Observation
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Observation.

    class STATUS(models.TextChoices):
        REGISTERED = "registered"
        PRELIMINARY = "preliminary"
        FINAL = "final"
        AMENDED = "amended"

    status = models.CharField(
        max_length=16, choices=STATUS, help_text="The status of the result value."
    )

    category = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.OBSERVATION_CATEGORY_CODE},
        help_text="A code that classifies the general type of observation being made.",
        related_name="observationcategory",
    )
    code = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_OBSERVATION_TYPE},
        help_text="Type of observation (code / type)",
        related_name="observationcode",
    )
    performer = models.ManyToManyField(
        Organization,
        help_text="Who is responsible for the observation",
    )
    subject = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Who and/or what the observation is about",
    )

    effectiveDateTime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Clinically relevant time/time-period for observation",
    )
    effectiveInstant = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Clinically relevant time/time-period for observation",
    )
    valueQuantity = models.JSONField(null=True, blank=True)
    hasMember = models.ManyToManyField("self")


class ObservationComponent(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    code = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_OBSERVATION_TYPE},
    )
    valueQuantity = models.JSONField(null=True, blank=True)


class ObservationIdentifier(Identifier):
    class SYSTEM(models.TextChoices):
        ODS_ORGANISATION_CODE = "https://fhir.nhs.uk/Id/ods-organization-code"
        ODS_SITE_CODE = "https://fhir.nhs.uk/Id/ods-site-code"
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
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    observation = models.ForeignKey(
        Observation,
        on_delete=models.CASCADE,
    )
