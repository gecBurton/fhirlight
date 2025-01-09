from django.db import models
from api.models.common import BaseProfile
from api.models.datatypes import Concept


class FamilyMemberHistoryProfile(BaseProfile):
    """This profile allows exchange of information about health events and conditions for a person related to the
    patient relevant in the context of care.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-FamilyMemberHistory
    # Current Version	1.1.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource FamilyMemberHistory.

    class STATUS(models.TextChoices):
        PARTIAL = "partial"
        COMPLETED = "completed"
        HEALTH_UNKNOWN = "health-unknown"
        ENTERED_IN_ERROR = "entered-in-error"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="A code specifying the status of the record of the family history of a specific family member.",
    )

    patient = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="The person who this history concerns.",
        related_name="FamilyMemberHistory_patient",
    )

    date = models.DateTimeField(
        help_text="The date (and possibly time) when the family member history was recorded or last updated."
    )
    bornDate = models.DateField(help_text="(approximate) date of birth")

    relationship = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_PERSON_RELATIONSHIP_TYPE
        },
        help_text="Relationship to the subject.",
        related_name="FamilyMemberHistory_relationship",
    )
    sex = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.ADMINISTRATIVE_GENDER},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The birth sex of the family member.",
        related_name="FamilyMemberHistory_sex",
    )
    name = models.CharField(
        max_length=256, null=True, blank=True, help_text="The family member described"
    )


class FamilyMemberHistoryCondition(models.Model):
    """Condition that the related person had."""

    profile = models.ForeignKey(
        FamilyMemberHistoryProfile,
        on_delete=models.CASCADE,
    )
    code = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={
            "valueset": Concept.VALUESET.CONDITION_PROBLEM_DIAGNOSIS_CODE
        },
        help_text="Condition suffered by relation",
        related_name="FamilyMemberHistoryCondition_code",
    )

    onsetAgeValue = models.PositiveIntegerField(null=True, blank=True)
    onsetAgeUnit = models.CharField(max_length=256, null=True, blank=True)
    onsetAgeSystem = models.URLField(null=True, blank=True)
    onsetAgeCode = models.CharField(max_length=256, null=True, blank=True)
