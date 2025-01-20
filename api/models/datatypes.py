import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import UniqueConstraint

from api.fields import PeriodField, QuantityField, TimingField


class Coding(models.Model):
    system = models.URLField(null=True, blank=True)
    version = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=256, null=True, blank=True)
    display = models.TextField(null=True, blank=True)
    userSelected = models.BooleanField(null=True, blank=True)

    class Meta:
        abstract = True


class DataTypeWithPeriod(models.Model):
    uuid = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid.uuid4
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    period = PeriodField(
        null=True,
        blank=True,
        help_text="Start time period when the record was/is in use",
    )

    class Meta:
        abstract = True


class ContactPoint(DataTypeWithPeriod):
    class SYSTEM(models.TextChoices):
        PHONE = "phone"
        FAX = "fax"
        EMAIL = "email"
        PAGER = "pager"
        URL = "url"
        SMS = "sms"
        OTHER = "other"

    class USE(models.TextChoices):
        HOME = "home"
        WORK = "work"
        TEMP = "temp"
        OLD = "old"
        MOBILE = "mobile"

    system = models.CharField(
        max_length=8,
        choices=SYSTEM,
        help_text="Telecommunications form for contact point - what communications system is required to make use of the contact.",
    )
    value = models.TextField(help_text="The actual contact point details.")
    use = models.CharField(
        null=True,
        blank=True,
        max_length=8,
        choices=USE,
        help_text="purpose of this contact point",
    )
    rank = models.PositiveIntegerField(
        null=True, blank=True, help_text="Specify preferred order of use (1 = highest)"
    )
    period = PeriodField(
        null=True,
        blank=True,
        help_text="Start time period when the contact point was/is in use",
    )

    class Meta:
        abstract = True


class Address(DataTypeWithPeriod):
    class USE(models.TextChoices):
        HOME = "home"
        WORK = "work"
        TEMP = "temp"
        OLD = "old"
        BILLING = "billing"

    class TYPE(models.TextChoices):
        POSTAL = "postal"
        PHYSICAL = "physical"
        BOTH = "both"

    use = models.CharField(
        null=True,
        blank=True,
        max_length=8,
        choices=USE,
        help_text="The purpose of this address.",
    )
    type = models.CharField(
        null=True,
        blank=True,
        max_length=8,
        choices=TYPE,
        help_text="Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.",
    )
    line = ArrayField(
        models.TextField(),
        null=True,
        blank=True,
        help_text="This component contains the house number, apartment number, street name, street direction, P.O. Box number, delivery hints, and similar address information.",
    )
    city = models.TextField(
        null=True,
        blank=True,
        help_text="The name of the city, town, suburb, village or other community or delivery center.",
    )
    district = models.TextField(
        null=True, blank=True, help_text="The name of the administrative area (county)."
    )
    state = models.TextField(
        null=True,
        blank=True,
        help_text="Sub-unit of a country with limited sovereignty in a federally organized country. A code may be used if codes are in common use (e.g. US 2 letter state codes).",
    )
    postalCode = models.TextField(
        null=True,
        blank=True,
        help_text="A postal code designating a region defined by the postal service.",
    )
    country = models.TextField(
        null=True,
        blank=True,
        help_text="Country - a nation as commonly understood or generally accepted.",
    )

    class Meta:
        abstract = True


class Identifier(DataTypeWithPeriod):
    class USE(models.TextChoices):
        USUAL = "usual"
        OFFICIAL = "official"
        TEMP = "temp"
        SECONDARY = "secondary"
        OLD = "old"

    use = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        choices=USE,
        help_text="The purpose of this identifier.",
    )
    # type This is not required with ODS
    value = models.TextField(
        help_text="The portion of the identifier typically relevant to the user and which is unique within the context of the system."
    )

    class Meta:
        abstract = True


class Name(DataTypeWithPeriod):
    """https://simplifier.net/guide/uk-core-implementation-guide-stu3-sequence/Home/Guidance/DataTypeGuidance/HumanName?version=1.7.0"""

    class USE(models.TextChoices):
        USUAL = "usual"
        OFFICIAL = "official"
        TEMP = "temp"
        NICKNAME = "nickname"
        ANONYMOUS = "anonymous"
        OLD = "old"
        MAIDEN = "maiden"

    use = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        choices=USE,
        help_text="The purpose of this identifier.",
    )
    family = models.TextField(
        null=True, blank=True, help_text="Family name (often called 'Surname')."
    )
    given = ArrayField(
        models.TextField(),
        null=True,
        blank=True,
        help_text="Given names (not always 'first'). Includes middle names.",
    )
    prefix = ArrayField(
        models.TextField(),
        null=True,
        blank=True,
        help_text="Part of the name that is acquired as a title due to academic, legal, employment or nobility status, etc. and that appears at the start of the name.",
    )
    suffix = ArrayField(
        models.TextField(),
        null=True,
        blank=True,
        help_text="Part of the name that is acquired as a title due to academic, legal, employment or nobility status, etc. and that appears at the end of the name.",
    )

    class Meta:
        abstract = True


class Concept(models.Model):
    class VALUESET(models.TextChoices):
        ADMINISTRATIVE_GENDER = "AdministrativeGender"
        ALLERGY_INTOLERANCE_CLINICAL_STATUS_CODE = (
            "AllergyIntoleranceClinicalStatusCodes"
        )
        ALLERGY_INTOLERANCE_VERIFICATION_STATUS_CODE = (
            "AllergyIntoleranceVerificationStatusCodes"
        )
        APPOINTMENT_CANCELLATION_REASON = "AppointmentCancellationReason"
        AS_NEEDED_CODEABLE_CONCEPT = "asNeededCodeableConcept"
        B5_STANDARD_SOP_CLASSES = "StandardSOPClasses"
        CID_29_ACQUISITION_MODALITY = "CID29AcquisitionModality"
        CONDITION_CLINICAL_STATUS_CODE = "ConditionClinicalStatusCodes"
        CONDITION_DIAGNOSIS_SEVERITY = "Condition/DiagnosisSeverity"
        CONDITION_PROBLEM_DIAGNOSIS_CODE = "Condition/Problem/DiagnosisCodes"
        CONDITION_STAGE = "ConditionStage"
        CONDITION_STAGE_TYPE = "ConditionStageType"
        CONDITION_VERIFICATION_STATUS = "ConditionVerificationStatus"
        CONSENT_CATEGORY_CODE = "ConsentCategoryCodes"
        CONSENT_SCOPE_CODE = "ConsentScopeCodes"
        CONSENT_STATE = "ConsentState"
        DEGREE_LICENSE_CERTIFICATE = "v2.0360.2.7"
        DIAGNOSTIC_SERVICE_SECTION_CODE = "DiagnosticServiceSectionCodes"
        DOSE_AND_RATE_TYPE_CODE = "DoseAndRateType"
        ENCOUNTER_REASON_CODE = "EncounterReasonCodes"
        EPISODE_OF_CARE_TYPE = "EpisodeOfCareType"
        FHIR_SPECIMEN_COLLECTION_METHOD = "FHIRSpecimenCollectionMethod"
        FLAG_CATEGORY = "FlagCategory"
        FLAG_CODE = "FlagCode"
        HEALTHCARE_SERVICE_CHARACTERISTIC = "HealthcareServiceCharacteristic"
        MANIFESTATION_AND_SYMPTOM_CODE = "ManifestationAndSymptomCodes"
        MEDICATION_CODEABLE_CONCEPT = "MedicationCodeableConcept"
        OBSERVATION_CATEGORY_CODE = "ObservationCategoryCodes"
        PARTICIPANT_TYPE = "ParticipantType"
        PRACTITIONER_ROLE = "PractitionerRole"
        PROCEDURE_PERFORMER_ROLE_CODE = "ProcedurePerformerRoleCodes"
        REFERRAL_METHOD = "ReferralMethod"
        SERVICE_CATEGORY = "ServiceCategory"
        SERVICE_DELIVERY_LOCATION_ROLE_TYPE = "ServiceDeliveryLocationRoleType"
        SERVICE_PROVISION_CONDITIONS = "ServiceProvisionConditions"
        SERVICE_REQUEST_CATEGORY_CODE = "ServiceRequestCategoryCodes"
        SERVICE_TYPE = "ServiceType"
        SNOMED_CT_BODY_STRUCTURES = "SNOMEDCTBodyStructures"
        TASK_CODE = "TaskCode"
        TASK_OUTPUT_TYPE_CODE = "TaskOutput"
        UK_CORE_ALLERGY_CODE = "UKCoreAllergyCode"
        UK_CORE_ALLERGY_SUBSTANCE = "UKCoreAllergySubstance"
        UK_CORE_APPOINTMENT_REASON_CODE = "UKCoreAppointmentReasonCode"
        UK_CORE_BODY_SITE = "UKCoreBodySite"
        UK_CORE_COMPOSITION_SECTION_CODE = "UKCoreCompositionSectionCode"
        UK_CORE_CONDITION_CATEGORY = "UKCoreConditionCategory"
        UK_CORE_CONDITION_CODE = "UKCoreConditionCode"
        UK_CORE_DEVICE_TYPE = "UKCoreDeviceType"
        UK_CORE_DISCHARGE_DESTINATION = "UKCoreDischargeDestination"
        UK_CORE_DOCUMENT_TYPE = "UKCoreDocumentType"
        UK_CORE_ENCOUNTER_TYPE = "UKCoreEncounterType"
        UK_CORE_HUMAN_LANGUAGE = "UKCore-HumanLanguage"
        UK_CORE_LIST_CODE = "UKCoreListCode"
        UK_CORE_LIST_EMPTY_REASON_CODE = "UKCoreListEmptyReasonCode"
        UK_CORE_MEDICATION_CODE = "UKCoreMedicationCode"
        UK_CORE_MEDICATION_DOSAGE_METHOD = "UKCoreMedicationDosageMethod"
        UK_CORE_MEDICATION_FORM = "UKCoreMedicationForm"
        UK_CORE_MEDICATION_REQUEST_CATEGORY_CODE = "UKCoreMedicationRequestCategory"
        UK_CORE_MEDICATION_STATEMENT_CATEGORY_CODE = "UKCoreMedicationStatementCategory"
        UK_CORE_OBSERVATION_TYPE = "UKCoreObservationType"
        UK_CORE_OPERATION_OUTCOME_ISSUE_DETAILS = "UKCoreOperationOutcomeIssueDetails"
        UK_CORE_ORGANIZATION_TYPE = "UKCoreOrganizationType"
        UK_CORE_PERSON_RELATIONSHIP_TYPE = "UKCorePersonRelationshipType"
        UK_CORE_PRACTICE_SETTINGS_CODE = "UKCorePracticeSettingCode"
        UK_CORE_PROCEDURE_CODE = "UKCoreProcedureCode"
        UK_CORE_REPORT_CODE = "UKCoreReportCode"
        UK_CORE_SERVICE_REQUEST_REASON_CODE = "UKCoreServiceRequestReasonCode"
        UK_CORE_SPECIMEN_BODY_SITE = "UKCoreSpecimenBodySite"
        UK_CORE_SPECIMEN_TYPE = "UKCoreSpecimenType"
        UK_CORE_SUBSTANCE_OR_PRODUCT_ADMINISTRATION_ROUTE = (
            "UKCoreSubstanceOrProductAdministrationRoute"
        )
        UK_CORE_VACCINE_CODE = "UKCoreVaccineCode"
        V2_0276 = "v2.0276"
        V3_ACT_ENCOUNTER_CODE = "v3.ActEncounterCode"
        V3_PURPOSE_OF_USE = "v3.PurposeOfUse"
        V3_SERVICE_DELIVERY_LOCATION_ROLE_TYPE = "v3.ServiceDeliveryLocationRoleType"

    system = models.CharField(
        null=True,
        blank=True,
        max_length=256,
        help_text="The identification of the code system that defines the meaning of the symbol in the code.",
    )
    version = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="Version of the system - if relevant",
    )
    code = models.CharField(
        max_length=128,
        help_text="Symbol in syntax defined by the system",
    )
    display = models.TextField(
        null=True,
        blank=True,
        help_text="A representation of the meaning of the code in the system, following the rules of the system.",
    )
    valueset = models.CharField(max_length=128, choices=VALUESET)
    # userSelected	Σ	0..1	boolean

    class Meta:
        constraints = [
            UniqueConstraint(fields=["code", "valueset"], name="unique_code_valueset")
        ]


class Dosage(DataTypeWithPeriod):
    """Dosage instructions for the medication"""

    text = models.TextField(
        null=True, blank=True, help_text="Free text dosage instructions."
    )

    site = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_BODY_SITE},
        help_text="Body site to administer to",
        related_name="Dosage_site",
    )
    route = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_SUBSTANCE_OR_PRODUCT_ADMINISTRATION_ROUTE
        },
        help_text="How drug should enter body",
        related_name="Dosage_route",
    )
    method = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_MEDICATION_DOSAGE_METHOD
        },
        help_text="Technique for administering medication",
        related_name="Dosage_method",
    )

    timing = TimingField(
        null=True, blank=True, help_text="Event occurs frequency times per period"
    )

    asNeededCodeableConcept = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.AS_NEEDED_CODEABLE_CONCEPT},
        help_text="The kind of dose or rate specified",
        related_name="Dosage_asNeededCodeableConcept",
    )


class DoseAndRate(DataTypeWithPeriod):
    type = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.DOSE_AND_RATE_TYPE_CODE},
        help_text="The kind of dose or rate specified",
        related_name="MedicationRequestDosageInstructionDoseAndRate_type",
    )
    doseQuantity = QuantityField(
        null=True, blank=True, help_text="Numerical value (with implicit precision)"
    )
