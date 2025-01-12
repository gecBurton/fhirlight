from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Identifier, ContactPoint, DataTypeWithPeriod


class QuestionnaireProfile(BaseProfile):
    """This profile is used to organise a collection of questions intended to solicit information from patients,
    providers or other individuals involved in the healthcare domain.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Questionnaire
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Questionnaire.

    class STATUS(models.TextChoices):
        DRAFT = "draft"
        ACTIVE = "active"
        RETIRED = "retired"
        UNKNOWN = "unknown"

    class SUBJECT_TYPE(models.TextChoices):
        ALLERGY_INTOLERANCE = "AllergyIntolerance"
        APPOINTMENT = "Appointment"
        COMPOSITION = "Composition"
        CONDITION = "Condition"
        CONSENT = "Consent"
        DEVICE = "Device"
        DIAGNOSTIC_REPORT = "DiagnosticReport"
        ENCOUNTER = "Encounter"
        EPISODE_OF_CARE = "EpisodeOfCare"
        FAMILY_MEMBER_HISTORY = "FamilyMemberHistory"
        FLAG = "Flag"
        HEALTHCARE_SERVICE = "HealthcareService"
        IMAGING_STUDY = "ImagingStudy"
        IMMUNIZATION = "Immunization"
        LIST = "List"
        LOCATION = "Location"
        MEDICATION = "Medication"
        MEDICATION_ADMINISTRATION = "MedicationAdministration"
        MEDICATION_DISPENSE = "MedicationDispense"
        MEDICATION_REQUEST = "MedicationRequest"
        MEDICATION_STATEMENT = "MedicationStatement"
        MESSAGE_HEADER = "MessageHeader"
        OBSERVATION = "Observation"
        OPERATION_OUTCOME = "OperationOutcome"
        ORGANIZATION = "Organization"
        PATIENT = "Patient"
        PRACTITIONER = "Practitioner"
        PRACTITIONER_ROLE = "PractitionerRole"
        PROCEDURE = "Procedure"
        QUESTIONNAIRE = "Questionnaire"
        QUESTIONNAIRE_RESPONSE = "QuestionnaireResponse"
        RELATED_PERSON = "RelatedPerson"
        SCHEDULE = "Schedule"
        SERVICE_REQUEST = "ServiceRequest"
        SLOT = "Slot"
        SPECIMEN = "Specimen"
        TASK = "Task"

    url = models.URLField(
        null=True,
        blank=True,
        help_text="Canonical identifier for this questionnaire, represented as a URI (globally unique).",
        unique=True,
    )
    status = models.CharField(
        max_length=8,
        choices=STATUS,
        help_text="The status of this questionnaire. Enables tracking the life-cycle of the content.",
    )
    title = models.CharField(
        null=True,
        blank=True,
        max_length=256,
        help_text="Name for this questionnaire (human friendly).",
    )
    experimental = models.BooleanField(
        null=True,
        blank=True,
        max_length=256,
        help_text="For testing purposes, not real usage.",
    )
    date = models.DateTimeField(null=True, blank=True, help_text="Date last changed")
    publisher = models.CharField(
        null=True,
        blank=True,
        max_length=256,
        help_text="Name of the publisher (organization or individual)",
    )
    purpose = models.TextField(
        null=True,
        blank=True,
        help_text="Intended jurisdiction for questionnaire (if applicable)",
    )
    subjectType = ArrayField(
        models.CharField(max_length=32, choices=SUBJECT_TYPE),
        null=True,
        blank=True,
        help_text="Resource that can be subject of QuestionnaireResponse.",
    )
    effectivePeriodStart = models.DateTimeField(
        null=True, blank=True, help_text="When the questionnaire is expected to be used"
    )
    effectivePeriodEnd = models.DateTimeField(
        null=True, blank=True, help_text="When the questionnaire is expected to be used"
    )


class QuestionnaireItem(DataTypeWithPeriod):
    """Questions and sections within the Questionnaire"""

    profile = models.ForeignKey(
        QuestionnaireProfile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class TYPE(models.TextChoices):
        GROUP = "group"
        DISPLAY = "display"
        BOOLEAN = "boolean"
        DECIMAL = "decimal"
        INTEGER = "integer"
        DATE = "date"
        DATE_TIME = "dateTime"
        STRING = "string"

    linkId = models.CharField(
        max_length=256, help_text="Unique id for item in questionnaire."
    )
    text = models.TextField(null=True, blank=True, help_text="The text of a question.")
    type = models.CharField(
        max_length=16,
        choices=TYPE,
        help_text="Defines the format in which the user is to be prompted for the answer.",
    )
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)


class QuestionnaireIdentifier(Identifier):
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

    profile = models.ForeignKey(
        QuestionnaireProfile,
        on_delete=models.CASCADE,
    )


class QuestionnaireContact(ContactPoint):
    profile = models.ForeignKey(QuestionnaireProfile, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="Name of an individual to contact",
    )
