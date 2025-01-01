from django.db import models

from api.models.common import UKCore
from api.models.datatypes import Concept


class Medication(UKCore):
    """This profile is primarily used for the identification and definition of a medication for the purposes of
    prescribing, dispensing, and administering a medication as well as for making statements about medication use.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Medication
    # Current Version	2.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Medication.

    class STATUS(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"
        ENTERED_IN_ERROR = "entered-in-error"

    status = models.CharField(
        null=True,
        blank=True,
        max_length=16,
        choices=STATUS,
        help_text="A code to indicate if the medication is in active use.",
    )

    code = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_MEDICATION_CODE},
        help_text="Codes that identify this medication",
        related_name="medicationcode",
    )
    form = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_MEDICATION_FORM},
        help_text="Codes that identify this medication",
        related_name="medicationform",
    )
    batchLotNumber = models.CharField(
        max_length=256, null=True, blank=True, help_text="Identifier assigned to batch"
    )
    batchExpirationDate = models.DateTimeField(
        null=True, blank=True, help_text="When batch will expire"
    )
