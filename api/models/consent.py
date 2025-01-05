from api.models.common import BaseProfile
from django.db import models

from api.models.datatypes import Concept, DataTypeWithPeriod


class ConsentProfile(BaseProfile):
    """The purpose of this profile is to be used to express a Consent regarding Healthcare. There are four anticipated
    uses for the Consent Resource, all of which are written or verbal agreements by a healthcare consumer [grantor] or
    a personal representative, made to an authorised entity [grantee] concerning authorised or restricted actions with
    any limitations on purpose of use, and handling instructions to which the authorised entity SHALL comply:

    * Privacy Consent Directive: Agreement to collect, access, use or disclose (share) information.
    * Medical Treatment Consent Directive: Consent to undergo a specific treatment (or record of refusal to consent).
    * Research Consent Directive: Consent to participate in research protocol and information sharing required.
    * Advance Care Directives: Consent to instructions for potentially needed medical treatment (e.g. DNR).
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Consent
    # Current Version	2.3.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Consent.

    # Consent.
    # Consent.source[x]	The source from which this consent is taken

    class STATUS(models.TextChoices):
        DRAFT = "draft"
        PROPOSED = "proposed"
        ACTIVE = "active"
        REJECTED = "rejected"
        INACTIVE = "inactive"
        ENTERED_IN_ERROR = "entered-in-error"

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        help_text="Indicates the current state of this consent.",
    )

    dateTime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When this consent was issued / created / indexed.",
    )

    scope = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.CONSENT_SCOPE_CODE},
        on_delete=models.CASCADE,
        help_text="A selector of the type of consent being presented: ADR, Privacy, Treatment, Research.",
        related_name="Consent_scope",
    )

    category = models.ManyToManyField(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.CONSENT_CATEGORY_CODE},
        blank=True,
        help_text="The classification of the consent statement - for indexing/retrieval",
        related_name="Consent_category",
    )

    patient = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The patient/healthcare consumer to whom this consent applies.",
        related_name="Consent_patient",
    )

    performer = models.ManyToManyField(
        BaseProfile,
        limit_choices_to={
            "polymorphic_ctype__model__in": ["patientprofile", "practitionerprofile"]
        },
        blank=True,
        help_text="Who is agreeing to the policy and rules",
        related_name="Consent_performer",
    )

    organization = models.ManyToManyField(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        blank=True,
        help_text="The custodian of the consent",
        related_name="Consent_organization",
    )

    provisionPurpose = models.ManyToManyField(
        Concept,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.V3_PURPOSE_OF_USE},
        help_text="Context of activities covered by this rule",
        related_name="Consent_provisionPurpose",
    )


class ConsentPolicy(DataTypeWithPeriod):
    authority = models.URLField(
        null=True, blank=True, help_text="Enforcement source for policy."
    )
    uri = models.URLField(
        null=True, blank=True, help_text="Specific policy covered by this consent."
    )

    consent = models.ForeignKey(
        ConsentProfile,
        on_delete=models.CASCADE,
    )
