import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models


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
    period_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Start time period when the record was/is in use",
    )
    period_end = models.DateTimeField(
        null=True, blank=True, help_text="End time period when the record was/is in use"
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
    period_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Start time period when the contact point was/is in use",
    )
    period_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text="End time period when the contact point was/is in use",
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

    use = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        choices=USE,
        help_text="The purpose of this identifier.",
    )
    # type This is not required with ODS
    system = models.URLField(
        max_length=64,
        choices=SYSTEM,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )
    value = models.TextField(
        help_text="The portion of the identifier typically relevant to the user and which is unique within the context of the system."
    )
    # assigner Implicit for ODS codes - SHOULD be omitted


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


class Concept(models.Model):
    class VALUESET(models.TextChoices):
        UK_CORE_HUMAN_LANGUAGE = "UKCore-HumanLanguage"
        UK_CORE_MEDICATION_FORM = "UKCoreMedicationForm"
        UK_CORE_MEDICATION_CODE = "UKCoreMedicationCode"
        OBSERVATION_CATEGORY_CODE = "ObservationCategoryCodes"
        UK_CORE_OBSERVATION_TYPE = "UKCoreObservationType"
        UK_CORE_SPECIMEN_TYPE = "UKCoreSpecimenType"
        FHIR_SPECIMEN_COLLECTION_METHOD = "FHIRSpecimenCollectionMethod"
        UK_CORE_SPECIMEN_BODY_SITE = "UKCoreSpecimenBodySite"

    system = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="The identification of the code system that defines the meaning of the symbol in the code.",
    )
    version = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="Version of the system - if relevant",
    )
    code = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="Symbol in syntax defined by the system",
    )
    display = models.CharField(
        null=True,
        blank=True,
        max_length=128,
        help_text="A representation of the meaning of the code in the system, following the rules of the system.",
    )
    valueset = models.CharField(max_length=128, choices=VALUESET)
    # userSelected	Σ	0..1	boolean
