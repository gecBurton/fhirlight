from django.db import models

from api.fields import PeriodField
from api.models.common import BaseProfile
from api.models.datatypes import (
    Concept,
    Identifier,
    Dosage,
    DoseAndRate,
)


class MedicationStatementProfile(BaseProfile):
    """This profile allows exchange of a record of a medication that is being consumed by a patient.

    A MedicationStatement may indicate that the individual may be taking the medication now or has taken the medication
    in the past or will be taking the medication in the future. The source of this information can be the individual,
    significant other (such as a family member or spouse), or a clinician.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-MedicationStatement
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource MedicationStatement.

    class STATUS(models.TextChoices):
        ACTIVE = "active"
        COMPLETED = "completed"
        ENTERED_IN_ERROR = "entered-in-error"
        INTENDED = "intended"
        STOPPED = "stopped"
        ON_HOLD = "on-hold"
        UNKNOWN = "unknown"
        NOT_TAKEN = "not-taken"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="A code representing the patient or other source's judgment about the state of the medication used that this statement is about. Generally, this will be active or completed.",
    )

    category = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_MEDICATION_STATEMENT_CATEGORY_CODE
        },
        help_text="Indicates where the medication is expected to be consumed or administered.",
        related_name="MedicationStatement_category",
    )

    medicationCodeableConcept = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.MEDICATION_CODEABLE_CONCEPT},
        help_text="Identifies the medication being administered. This is the details of the medication or a simple attribute carrying a code that identifies the medication from a known list of medications.",
        related_name="MedicationStatement_medicationCodeableConcept",
    )

    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        help_text="The person, animal or group who is/was taking the medication.",
        related_name="MedicationStatement_subject",
    )

    effectivePeriod = PeriodField(
        null=True,
        blank=True,
        help_text="The interval of time during which it is being asserted that the patient is/was/will be taking the medication (or was not taking, when the MedicationStatement.taken element is No).",
    )

    dateAsserted = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date when the medication statement was asserted by the information source.",
    )

    reasonCode = models.ManyToManyField(
        Concept,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.CONDITION_PROBLEM_DIAGNOSIS_CODE
        },
        help_text="A reason for why the medication is being/was taken.",
        related_name="MedicationStatement_reasonCode",
    )


class MedicationStatementIdentifier(Identifier):
    class SYSTEM(models.TextChoices):
        UUID = "https://tools.ietf.org/html/rfc4122"

    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    profile = models.ForeignKey(MedicationStatementProfile, on_delete=models.CASCADE)


class MedicationStatementDosage(Dosage):
    """Dosage instructions for the medication"""

    profile = models.ForeignKey(MedicationStatementProfile, on_delete=models.CASCADE)


class MedicationStatementDosageDoseAndRate(DoseAndRate):
    profile = models.ForeignKey(
        MedicationStatementDosage,
        on_delete=models.CASCADE,
    )
