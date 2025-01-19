from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, DataTypeWithPeriod, Identifier


class AllergyIntoleranceProfile(BaseProfile):
    """This profile allows a record of a clinical assessment of an allergy or intolerance; a propensity, or a potential
    risk to an individual, to have an adverse reaction on future exposure to the specified substance, or class of
    substance.

    Where a propensity is identified, to record information or evidence about a reaction event that is characterised by
    any harmful or undesirable physiological response that is specific to the individual and triggered by exposure of
    an individual to the identified substance or class of substance.

    Substances include but are not limited to a therapeutic substance administered correctly at an appropriate dosage
    for the individual; food; material derived from plants or animals; or venom from insect stings.

    This resource is used to record physical conditions. It SHALL NOT be used to record preferences for or against
    types of treatment, for example on religious grounds. For such use cases consider the use of the FHIR Consent
    resource."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-AllergyIntolerance
    # Current Version	2.4.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource AllergyIntolerance.

    class TYPE(models.TextChoices):
        ALLERGY = "allergy"
        INTOLERANCE = "intolerance"

    class CATEGORY(models.TextChoices):
        FOOD = "food"
        MEDICATION = "medication"
        ENVIRONMENT = "environment"
        BIOLOGIC = "biologic"

    class CRITICALITY(models.TextChoices):
        LOW = "low"
        HIGH = "high"
        UNABLE_TO_ASSES = "unable-to-assess"

    clinicalStatus = models.ForeignKey(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.ALLERGY_INTOLERANCE_CLINICAL_STATUS_CODE
        },
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Defines whether the allergy or intolerance is active, inactive or resolved.",
        related_name="AllergyIntolerance_clinicalStatus",
    )

    verificationStatus = models.ForeignKey(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.ALLERGY_INTOLERANCE_VERIFICATION_STATUS_CODE
        },
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Defines the assertion of the allergy or intolerance.",
        related_name="AllergyIntolerance_verificationStatus",
    )

    type = models.CharField(
        max_length=16,
        choices=TYPE,
        null=True,
        blank=True,
        help_text="Identification of the underlying physiological mechanism for the reaction risk.",
    )

    category = ArrayField(
        models.CharField(
            max_length=16,
            choices=CATEGORY,
        ),
        null=True,
        blank=True,
        help_text="Category of the identified substance.",
    )

    criticality = models.CharField(
        max_length=16,
        choices=CRITICALITY,
        null=True,
        blank=True,
        help_text="Estimate of the potential clinical harm, or seriousness, of the reaction to the identified substance.",
    )

    code = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_ALLERGY_CODE},
        on_delete=models.CASCADE,
        help_text="Code that identifies the allergy or intolerance",
        related_name="AllergyIntolerance_code",
    )

    patient = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Links the allergy to the patient.",
        related_name="AllergyIntolerance_patient",
    )

    encounter = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        on_delete=models.CASCADE,
        help_text="Encounter when the allergy or intolerance was asserted",
        related_name="AllergyIntolerance_encounter",
    )

    onsetDateTime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Estimated or actual date, date-time, or age when allergy or intolerance was identified.",
    )

    recordedDate = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date first version of the resource instance was recorded",
    )

    recorder = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        help_text="Who recorded the sensitivity.",
        related_name="AllergyIntolerance_recorder",
    )

    asserter = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        help_text="Source of the information about the allergy",
        related_name="AllergyIntolerance_asserter",
    )

    lastOccurrence = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Represents the date and/or time of the last known occurrence of a reaction event.",
    )


class AllergyIntoleranceIdentifier(Identifier):
    profile = models.ForeignKey(
        AllergyIntoleranceProfile,
        on_delete=models.CASCADE,
    )
    system = models.URLField(
        max_length=64,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )


class AllergyIntoleranceReaction(DataTypeWithPeriod):
    """Adverse Reaction Events linked to exposure to substance"""

    class SEVERITY(models.TextChoices):
        MILD = "mild"
        MODERATE = "moderate"
        SEVERE = "severe"

    substance = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_ALLERGY_SUBSTANCE},
        help_text="Specific substance or pharmaceutical product considered to be responsible for event/",
        related_name="AllergyIntoleranceReaction_substance",
    )

    manifestation = models.ManyToManyField(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.ALLERGY_INTOLERANCE_VERIFICATION_STATUS_CODE
        },
        help_text="Clinical symptoms/signs associated with the Event",
    )

    description = models.TextField(
        null=True,
        blank=True,
        help_text="Text description about the reaction as a whole, including details of the manifestation if required.",
    )

    onset = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Record of the date and/or time of the onset of the Reaction.",
    )

    severity = models.CharField(
        max_length=16, choices=SEVERITY, null=True, blank=True, help_text=""
    )

    exposureRoute = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_SUBSTANCE_OR_PRODUCT_ADMINISTRATION_ROUTE
        },
        help_text="Identification of the route by which the subject was exposed to the substance.",
        related_name="AllergyIntoleranceReaction_exposureRoute",
    )

    profile = models.ForeignKey(
        AllergyIntoleranceProfile,
        on_delete=models.CASCADE,
    )
