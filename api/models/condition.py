from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, DataTypeWithPeriod, Identifier


class ConditionProfile(BaseProfile):
    """This profile allows recording of detailed information about a condition, problem, diagnosis, or other event,
    situation, issue, or clinical concept that has risen to a level of concern.

    The condition could be a point in time diagnosis in the context of an encounter, it could be an item on the
    practitioner’s problem list, or it could be a concern that doesn’t exist on the practitioner’s problem list. Often,
    a condition is about a clinician's assessment and assertion of a particular aspect of an individual's state of
    health.

    It can be used to record information about a disease/illness identified from application of clinical reasoning over
    the pathologic and pathophysiologic findings (diagnosis), or identification of health issues/situations that a
    practitioner considers harmful, potentially harmful and may be investigated and managed (problem), or other health
    issue/situation that may require ongoing monitoring and/or management (health issue/concern).
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Condition
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Condition.

    clinicalStatus = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.CONDITION_CLINICAL_STATUS_CODE},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The clinical status of the condition.",
        related_name="DiagnosticReport_clinicalStatus",
    )

    verificationStatus = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.CONDITION_VERIFICATION_STATUS},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The verification status to support the clinical status of the condition.",
        related_name="DiagnosticReport_verificationStatus",
    )

    category = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_CONDITION_CATEGORY},
        blank=True,
        help_text="A category assigned to the condition.",
        related_name="DiagnosticReport_category",
    )

    severity = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.CONDITION_DIAGNOSIS_SEVERITY},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="A subjective assessment of the severity of the condition as evaluated by the clinician.",
        related_name="DiagnosticReport_severity",
    )

    code = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_CONDITION_CODE},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Identification of the condition, problem or diagnosis.",
        related_name="DiagnosticReport_code",
    )

    bodySite = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.SNOMED_CT_BODY_STRUCTURES},
        blank=True,
        help_text="The anatomical location where this condition manifests itself.",
        related_name="DiagnosticReport_bodySite",
    )

    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Indicates the patient or group who the condition record is associated with.",
        related_name="DiagnosticReport_subject",
    )

    encounter = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The Encounter during which this Condition was created or to which the creation of this record is tightly associated.",
        related_name="DiagnosticReport_encounter",
    )

    onsetDateTime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Estimated or actual date-time the condition began, in the opinion of the clinician.",
    )

    abatementDateTime = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date or estimated date that the condition resolved or went into remission. This is called "abatement" because of the many overloaded connotations associated with "remission" or "resolution" - Conditions are never really resolved, but they can abate.',
    )

    recordedDate = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The recordedDate represents when this particular Condition record was created in the system, which is often a system-generated date.",
    )

    recorder = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={
            "polymorphic_ctype__model__in": [
                "patientprofile",
                "practitionerprofile",
                "practitionerroleprofile",
                "relatedpersonprofile",
            ]
        },
        on_delete=models.CASCADE,
        help_text="Individual who recorded the record and takes responsibility for its content..",
        related_name="DiagnosticReport_recorder",
    )

    asserter = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={
            "polymorphic_ctype__model__in": [
                "practitionerprofile",
                "practitionerroleprofile",
                "patientprofile",
                "relatedpersonprofile",
            ]
        },
        on_delete=models.CASCADE,
        help_text="Individual who is making the condition statement.",
        related_name="DiagnosticReport_asserter",
    )


class ConditionIdentifier(Identifier):
    """An identifier for this device."""

    system = models.URLField(
        max_length=64,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.ForeignKey(
        ConditionProfile,
        on_delete=models.CASCADE,
    )


class ConditionStage(DataTypeWithPeriod):
    """Clinical stage or grade of a condition. May include formal severity assessments."""

    profile = models.ForeignKey(
        ConditionProfile,
        on_delete=models.CASCADE,
    )

    summary = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.CONDITION_STAGE},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='A simple summary of the stage such as "Stage 3". The determination of the stage is disease-specific.',
        related_name="ConditionStage_summary",
    )

    assessment = models.ManyToManyField(
        BaseProfile,
        limit_choices_to={
            "polymorphic_ctype__model__in": [
                "diagnosticreportprofile",
                "observationprofile",
            ]
        },
        blank=True,
        help_text="Reference to a formal record of the evidence on which the staging assessment is based.",
        related_name="ConditionStage_assessment",
    )

    type = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.CONDITION_STAGE_TYPE},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The kind of staging, such as pathological or clinical staging.",
        related_name="ConditionStage_type",
    )


class ConditionEvidence(DataTypeWithPeriod):
    """Supporting evidence / manifestations that are the basis of the Condition's verification status, such as evidence
    that confirmed or refuted the condition."""

    profile = models.ForeignKey(
        ConditionProfile,
        on_delete=models.CASCADE,
    )

    code = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.MANIFESTATION_AND_SYMPTOM_CODE},
        blank=True,
        help_text="A manifestation or symptom that led to the recording of this condition.",
        related_name="ConditionEvidence_code",
    )
