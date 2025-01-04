from django.db import models

from api.models.common import UKCore
from api.models.datatypes import Concept


class UKCoreImmunization(UKCore):
    """This profile is intended to cover the recording of current and historical administration of vaccines to
    individuals across all healthcare disciplines in all care settings and all regions.

    This profile does not support the administration of non-vaccine agents, even those that may have or claim to have
    immunological effects. While the terms "immunisation" and "vaccination" are not clinically identical, for the
    purposes of the FHIR profile, the terms are used synonymously.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Immunization
    # Current Version	2.3.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Immunization.
    class STATUS(models.TextChoices):
        completed = "completed"
        ENTERED_IN_ERROR = "entered-in-error"
        NOT_DONE = "not-done"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="Indicates the current status of the immunization event.",
    )

    vaccineCode = models.ForeignKey(
        Concept,
        on_delete=models.CASCADE,
        limit_choices_to=Concept.VALUESET.UK_CORE_VACCINE_CODE,
        help_text="Vaccine that was administered or was to be administered.",
    )
    patient = models.ForeignKey(
        UKCore,
        limit_choices_to={"polymorphic_ctype__model__in": ["ukcorepatient"]},
        on_delete=models.CASCADE,
        help_text="The patient who either received or did not receive the immunization.",
        related_name="Immunization_patient",
    )
    occurrenceDateTime = models.DateTimeField(
        help_text="vaccine administered or was to be administered."
    )
    manufacturer = models.ForeignKey(
        UKCore,
        limit_choices_to={"polymorphic_ctype__model__in": ["ukcoreorganization"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Name of vaccine manufacturer.",
        related_name="Immunization_manufacturer",
    )
    location = models.ForeignKey(
        UKCore,
        limit_choices_to={"polymorphic_ctype__model__in": ["ukcorelocation"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Where immunization occurred",
        related_name="Immunization_location",
    )
    lotNumber = models.CharField(
        max_length=256, blank=True, null=True, help_text="Lot number of the vaccine."
    )
    # Immunization.doseQuantity	How much of the vaccine was administered
