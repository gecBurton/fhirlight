from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, DataTypeWithPeriod


class ListProfile(BaseProfile):
    """This profile allows exchange of a flat, possibly ordered collection of records.

    The list profile can be used in many places, including allergies, medications, alerts, family history, medical
    history, etc. This list profile can be used to support individual-specific clinical lists as well as lists that
    manage workflows such as tracking patients, managing teaching cases, etc.

    The list profile supports lists that are homogeneous – consisting of only one type of resource (e.g. Allergy lists)
    as well as heterogeneous – containing a variety of resources (e.g. a problem list including Condition,
    AllergyIntolerance, Procedure, etc.).
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-List
    # Current Version	2.3.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource List.

    class STATUS(models.TextChoices):
        PRELIMINARY = "current"
        FINAL = "retired"
        ENTERED_IN_ERROR = "entered-in-error"

    class MODE(models.TextChoices):
        WORKING = "working"
        SNAPSHOT = "snapshot"
        CHANGES = "changes"

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        help_text="Indicates the current state of this list.",
    )

    code = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_LIST_CODE},
        on_delete=models.CASCADE,
        help_text="This code defines the purpose of the list - why it was created.",
        related_name="List_code",
    )

    mode = models.CharField(
        max_length=32,
        choices=MODE,
        help_text="How this list was prepared - whether it is a working list that is suitable for being maintained on an ongoing basis, or if it represents a snapshot of a list of items from another source, or whether it is a prepared list where items may be marked as added, modified or deleted.",
    )

    emptyReason = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_LIST_EMPTY_REASON_CODE},
        help_text="If the list is empty, why the list is empty.",
        related_name="List_emptyReason",
    )

    date = models.DateTimeField(
        null=True, blank=True, help_text="The date that the list was prepared."
    )

    subject = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The common subject (or patient) of the resources that are in the list if there is one.",
        related_name="List_subject",
    )


class ListEntry(DataTypeWithPeriod):
    profile = models.ForeignKey(
        ListProfile, on_delete=models.CASCADE, related_name="ListEntry_profile"
    )
    item = models.ForeignKey(
        BaseProfile, on_delete=models.CASCADE, related_name="ListEntry_item"
    )
