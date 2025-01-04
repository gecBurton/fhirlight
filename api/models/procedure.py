from django.db import models

from api.models.common import UKCore
from api.models.datatypes import Concept


class UKCoreProcedure(UKCore):
    """This profile allows exchange of details of current and historical procedures performed on or for an individual.
    A procedure is an activity that is performed on, with, or for an individual as part of the provision of care.
    Examples include surgical procedures, diagnostic procedures, endoscopic procedures, biopsies, counselling,
    physiotherapy, personal support services, adult day care services, non-emergency transportation, home modification,
    exercise, etc. Procedures may be performed by a healthcare professional, a service provider, a friend or relative
    or in some cases by themselves.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Procedure
    # Current Version	2.4.0
    # Last Updated	2023-04-28
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Procedure.

    class STATUS(models.TextChoices):
        PREPARATION = "preparation"
        IN_PROGRESS = "in-progress"
        NOT_DONE = "not-done"
        ON_HOLD = "on-hold"
        STOPPED = "stopped"
        COMPLETED = "completed"
        ENTERED_IN_ERROR = "entered-in-error"
        UNKNOWN = "unknown"

    status = models.CharField(
        max_length=32, help_text="A code specifying the state of the procedure."
    )
    code = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        limit_choices_to={"valueset": Concept.VALUESET.UK_CORE_PROCEDURE_CODE},
        max_length=32,
        help_text="A code specifying the state of the procedure.",
    )
    performedDateTime = models.DateTimeField(
        null=True, blank=True, help_text="Date and time the procedure was performed."
    )
    subject = models.ForeignKey(
        UKCore,
        limit_choices_to={"polymorphic_ctype__model__in": ["ukcorepatient"]},
        on_delete=models.CASCADE,
        help_text="Who the procedure was performed on",
        related_name="Procedure_subject",
    )
