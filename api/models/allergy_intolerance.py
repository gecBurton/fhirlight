from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, DataTypeWithPeriod


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

    # AllergyIntolerance.code	This code identifies the allergy or intolerance
    # AllergyIntolerance.reaction	Details about each adverse reaction event
    # AllergyIntolerance.reaction.severity	Clinical assessment of the severity of the reaction event as a whole

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
    code = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_ALLERGY_CODE},
        on_delete=models.CASCADE,
        help_text="Code that identifies the allergy or intolerance",
        related_name="AllergyIntolerance_code",
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

    recordedDate = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date first version of the resource instance was recorded",
    )


class AllergyIntoleranceReaction(DataTypeWithPeriod):
    """Adverse Reaction Events linked to exposure to substance"""

    class SEVERITY(models.TextChoices):
        MILD = "mild"
        MODERATE = "moderate"
        SEVERE = "severe"

    manifestation = models.ManyToManyField(
        Concept,
        limit_choices_to={
            "valueset": Concept.VALUESET.ALLERGY_INTOLERANCE_VERIFICATION_STATUS_CODE
        },
        help_text="Clinical symptoms/signs associated with the Event",
    )
    severity = models.CharField(
        max_length=16, choices=SEVERITY, null=True, blank=True, help_text=""
    )
    profile = models.ForeignKey(
        AllergyIntoleranceProfile,
        on_delete=models.CASCADE,
    )
