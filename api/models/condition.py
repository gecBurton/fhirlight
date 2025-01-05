from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept


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
        limit_choices_to={"valueset": Concept.VALUESET.CONDITION_DIAGNOSIS_Severity},
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

    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="Indicates the patient or group who the condition record is associated with.",
        related_name="DiagnosticReport_subject",
    )

    recorder = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        help_text="Individual who recorded the record and takes responsibility for its content..",
        related_name="DiagnosticReport_recorder",
    )
