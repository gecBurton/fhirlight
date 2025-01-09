from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, DataTypeWithPeriod


class CompositionProfile(BaseProfile):
    """This profile allows a record of a set of healthcare-related information that is assembled together into a single
    logical package that provides a single coherent statement of meaning, establishes its own context and that has
    clinical attestation with regard to who is making the statement.

    A Composition defines the structure and narrative content necessary for a document. However, a Composition alone
    does not constitute a document. Rather, the Composition SHALL be the first entry in a Bundle where
    Bundle.type=document, and any other resources referenced from Composition SHALL be included as subsequent entries
    in the Bundle, for example Patient, Practitioner, Encounter, etc.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Composition
    # Current Version	2.3.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Composition.

    # Composition.confidentiality	The code specifying the level of confidentiality of the Composition.
    # Composition.custodian

    class STATUS(models.TextChoices):
        PRELIMINARY = "preliminary"
        FINAL = "final"
        AMENDED = "amended"
        ENTERED_IN_ERROR = "entered-in-error"

    identifierValue = models.UUIDField(
        null=True,
        blank=True,
        help_text="Version-independent identifier for the Composition",
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        help_text="The workflow/clinical status of this composition.",
    )

    type = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_DOCUMENT_TYPE},
        on_delete=models.CASCADE,
        help_text="Specifies the particular kind of composition.",
        related_name="Composition_type",
    )

    date = models.DateTimeField(help_text="Composition editing time")

    title = models.TextField(help_text="Human Readable name/title")

    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Who and/or what the composition is about.",
        related_name="Composition_subject",
    )

    author = models.ManyToManyField(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        help_text="Identifies who is responsible for the information in the composition.",
        related_name="Composition_author",
    )

    encounter = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Who and/or what the composition is about",
        related_name="Composition_encounter",
    )

    custodian = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["organizationprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Organization which maintains the composition",
        related_name="Composition_custodian",
    )


class CompositionSection(DataTypeWithPeriod):
    """The clinical service(s) being documented"""

    class TEXT_STATUS(models.TextChoices):
        GENERATED = "generated"
        EXTENSIONS = "extensions"
        ADDITIONAL = "additional"
        EMPTY = "empty"

    title = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="Label for section (e.g. for ToC).",
    )
    code = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_COMPOSITION_SECTION_CODE
        },
        null=True,
        blank=True,
        help_text="Classification of section (recommended).",
    )

    entry = models.ManyToManyField(
        BaseProfile,
        blank=True,
        help_text="A reference to data that supports this section",
        related_name="CompositionSection_entry",
    )

    profile = models.ForeignKey(
        CompositionProfile,
        on_delete=models.CASCADE,
    )
