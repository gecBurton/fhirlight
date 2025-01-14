from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Identifier, DataTypeWithPeriod
from api.models.questionnaire import QuestionnaireBase


class QuestionnaireResponseProfile(QuestionnaireBase):
    """This profile describes a structured set of questions and their answers. The questions are ordered and grouped
    into coherent subsets, corresponding to the structure of the grouping of the questionnaire being responded to.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-QuestionnaireResponse
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource QuestionnaireResponse.

    class STATUS(models.TextChoices):
        IN_PROGRESS = "in-progress"
        COMPLETED = "completed"
        AMENDED = "amended"
        ENTERED_IN_ERROR = "entered-in-error"
        STOPPED = "stopped"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="The status of this questionnaire. Enables tracking the life-cycle of the content.",
    )

    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="The subject of the questions",
        related_name="QuestionnaireResponse_subject",
    )

    author = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The subject of the questions",
        related_name="QuestionnaireResponse_author",
    )

    encounter = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        on_delete=models.CASCADE,
        help_text="The subject of the questions",
        related_name="QuestionnaireResponse_encounter",
    )

    source = models.ForeignKey(
        BaseProfile,
        null=True,
        blank=True,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="The subject of the questions",
        related_name="QuestionnaireResponse_source",
    )

    authored = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date and/or time that this set of answers were last changed.",
    )
    questionnaire = models.URLField(
        null=True, blank=True, help_text="Form being answered"
    )


class QuestionnaireResponseIdentifier(Identifier):
    """The address of the organisation using the Address datatype."""

    class SYSTEM(models.TextChoices):
        ODS_ORGANISATION_CODE = "https://fhir.nhs.uk/Id/ods-organization-code"
        ODS_SITE_CODE = "https://fhir.nhs.uk/Id/ods-site-code"

    system = models.URLField(
        max_length=64,
        null=True,
        blank=True,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.OneToOneField(
        QuestionnaireResponseProfile,
        on_delete=models.CASCADE,
    )


class QuestionnaireResponseItem(DataTypeWithPeriod):
    """Questions and sections within the Questionnaire"""

    profile = models.ForeignKey(
        QuestionnaireResponseProfile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    linkId = models.CharField(
        max_length=256, help_text="Unique id for item in questionnaire."
    )
    text = models.TextField(null=True, blank=True, help_text="The text of a question.")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    answer = models.JSONField(null=True, blank=True)
