from django.db import models

from api.models.common import BaseProfile
from api.models.datatypes import Concept, Identifier, DataTypeWithPeriod


class TaskProfile(BaseProfile):
    """A task resource describes an activity that can be performed and tracks the state of completion of that activity.
    It is a representation that an activity should be or has been initiated, and eventually, represents the successful
    or unsuccessful completion of that activity.

    Note that there are a variety of processes associated with making and processing orders. Some orders may be handled
    immediately by automated systems but most require real world actions by one or more humans. Some orders can only be
    processed when other real world actions happen, such as a patient presenting themselves so that the action to be
    performed can actually be performed. Often these real world dependencies are only implicit in the order details.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-Task
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource Task.

    class STATUS(models.TextChoices):
        DRAFT = "draft"
        REQUESTED = "requested"
        RECEIVED = "received"
        ACCEPTED = "accepted"
        IN_PROGRESS = "in-progress"

    class INTENT(models.TextChoices):
        UNKNOWN = "unknown"
        PROPOSAL = "proposal"
        PLAN = "plan"
        ORDER = "order"
        ORIGINAL_ORDER = "original-order"
        REFLEX_ORDER = "reflex-order"
        FILLER_ORDER = "filler-order"
        INSTANCE_ORDER = "instance-order"
        INSTANCE_OPTION = "instance-option"

    class PRIORITY(models.TextChoices):
        ROUTINE = "routine"
        URGENT = "urgent"
        ASAP = "asap"
        STAT = "stat"

    status = models.CharField(
        max_length=16,
        choices=STATUS,
        help_text="The current status of the task.",
    )

    intent = models.CharField(
        max_length=16,
        choices=INTENT,
        help_text='Indicates the "level" of actionability associated with the Task, i.e. i+R[9]Cs this a proposed task, a planned task, an actionable task, etc.',
    )

    priority = models.CharField(
        max_length=16,
        choices=PRIORITY,
        help_text="Indicates how quickly the Task should be addressed with respect to other requests.",
    )

    code = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.TASK_CODE},
        on_delete=models.CASCADE,
        help_text="A name or code (or both) briefly describing what the task involves.",
        related_name="Task_code",
    )

    focus = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["servicerequestprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The request being actioned or the resource being manipulated by this task.",
        related_name="Task_focus",
    )

    _for = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["patientprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The entity who benefits from the performance of the service specified in the task (e.g., the patient).",
        related_name="Task_for",
    )

    encounter = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["encounterprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The healthcare event (e.g. a patient and healthcare provider interaction) during which this task was created.",
        related_name="Task_encounter",
    )

    requester = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Who is asking for task to be done.",
        related_name="Task_requester",
    )

    owner = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["practitionerprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Responsible individual.",
        related_name="Task_owner",
    )

    executionPeriodStart = models.DateTimeField(
        null=True, blank=True, help_text="Start time of execution"
    )
    executionPeriodEnd = models.DateTimeField(
        null=True, blank=True, help_text="End time of execution"
    )
    authoredOn = models.DateTimeField(
        null=True, blank=True, help_text="Task creation date."
    )
    lastModified = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date and time of last modification to this task.",
    )
    restrictionPeriodStart = models.DateTimeField(
        null=True, blank=True, help_text="When fulfillment should start."
    )
    restrictionPeriodEnd = models.DateTimeField(
        null=True, blank=True, help_text="When fulfillment should end."
    )
    restrictionRepetitions = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Indicates the number of times the requested action should occur.",
    )
    performerType = models.ManyToManyField(
        Concept,
        blank=True,
        limit_choices_to={"valueset": Concept.VALUESET.PROCEDURE_PERFORMER_ROLE_CODE},
        help_text="A name or code (or both) briefly describing what the task involves.",
        related_name="Task_performerType",
    )


class TaskIdentifier(Identifier):
    """External Ids for this item"""

    system = models.URLField(
        max_length=64,
        help_text="Establishes the namespace for the value - that is, a URL that describes a set values that are unique.",
    )

    profile = models.ForeignKey(
        TaskProfile,
        on_delete=models.CASCADE,
    )


class TaskOutput(DataTypeWithPeriod):
    """Information produced as part of task"""

    profile = models.ForeignKey(
        TaskProfile,
        on_delete=models.CASCADE,
    )

    valueReference = models.ForeignKey(
        BaseProfile,
        limit_choices_to={"polymorphic_ctype__model__in": ["servicerequestprofile"]},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Result of output.",
        related_name="TaskOutput_valueReference",
    )

    type = models.ForeignKey(
        Concept,
        limit_choices_to={"valueset": Concept.VALUESET.TASK_OUTPUT_TYPE_CODE},
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Label for output",
        related_name="TaskOutput_type",
    )
