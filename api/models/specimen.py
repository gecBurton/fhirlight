from django.db import models

from api.models.common import UKCore
from api.models.datatypes import Concept


class UKCoreSpecimen(UKCore):
    """This profile allows exchange of information about a sample to be used for analysis."""

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Specimen
    # Current Version	2.3.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Specimen.

    # Specimen.request	Why the specimen was collected.
    class STATUS(models.TextChoices):
        AVAILABLE = "available"
        UNAVAILABLE = "unavailable"
        UNSATISFACTORY = "unsatisfactory"
        ENTERED_IN_ERROR = "entered-in-error"

    status = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        choices=STATUS,
        help_text="The availability of the specimen.",
    )
    type = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_SPECIMEN_TYPE},
        on_delete=models.CASCADE,
        help_text="The kind of material that forms the specimen.",
    )
    subject = models.ForeignKey(
        UKCore,
        limit_choices_to={"polymorphic_ctype__model__in": ["ukcorepatient"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Where the specimen came from.",
        related_name="specimen_patient",
    )
    receivedTime = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The time when specimen was received for processing.",
    )

    method = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.FHIR_SPECIMEN_COLLECTION_METHOD},
        related_name="specimenmethod",
    )
    collector = models.ForeignKey(
        UKCore,
        limit_choices_to={"polymorphic_ctype__model__in": ["ukcorepractitioner"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="specimen_practitioner",
    )
    collectedDateTime = models.DateTimeField(null=True, blank=True)
    bodySite = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_SPECIMEN_BODY_SITE},
        related_name="specimenbodysite",
    )
