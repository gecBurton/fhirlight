from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.models.common import UKCore
from api.models.datatypes import Concept, DataTypeWithPeriod


class UKCoreOperationOutcome(UKCore):
    """The purpose of this profile is to provide detailed information about the outcome of an attempted system
    operation. Operation outcomes are sets of error, warning and information messages provided as a direct system
    response, or part of one, and provide information about the outcome of the operation.
    """

    # Canonical URL	https://fhir.hl7.org.uk/StructureDefinition/UKCore-OperationOutcome
    # Current Version	1.2.0
    # Last Updated	2022-12-16
    # Description	This profile defines the UK constraints and extensions on the International FHIR resource OperationOutcome.


class OperationOutcomeIssue(DataTypeWithPeriod):
    operation_outcome = models.ForeignKey(
        UKCoreOperationOutcome, on_delete=models.CASCADE
    )

    class SEVERITY(models.TextChoices):
        FATAL = "fatal"
        ERROR = "error"
        WARNING = "warning"
        INFORMATION = "information"

    class CODE(models.TextChoices):
        CODE = "Code"
        INVALID = "invalid"
        STRUCTURE = "structure"
        REQUIRED = "required"
        VALUE = "value"
        INVARIANT = "invariant"
        SECURITY = "security"
        LOGIN = "login"
        UNKNOWN = "unknown"
        EXPIRED = "expired"
        FORBIDDEN = "forbidden"
        SUPPRESSED = "suppressed"
        PROCESSING = "processing"
        NOT_SUPPORTED = "not-supported"
        DUPLICATE = "duplicate"
        MULTIPLE_MATCHES = "multiple-matches"
        NOT_FOUND = "not-found"
        DELETED = "deleted"
        TOO_LONG = "too-long"
        CODE_INVALID = "code-invalid"
        EXTENSION = "extension"
        TOO_COSTLY = "too-costly"
        BUSINESS_RULE = "business-rule"
        CONFLICT = "conflict"
        TRANSIENT = "transient"
        LOCK_ERROR = "lock-error"
        NO_STORE = "no-store"
        EXCEPTION = "exception"
        TIMEOUT = "timeout"
        INCOMPLETE = "incomplete"
        THROTTLED = "throttled"
        INFORMATIONAL = "informational"

    severity = models.CharField(
        max_length=16,
        choices=SEVERITY,
        help_text='Indicates how relevant the issue is to the overall success of the action. This is labelled as "Is Modifier" because applications should not confuse hints and warnings with errors.',
    )
    code = models.CharField(
        max_length=64,
        choices=CODE,
        help_text="Error or warning code",
    )
    expression = ArrayField(
        models.TextField(),
        null=True,
        blank=True,
        help_text="FFHIRPath of element(s) related to issue",
    )
    diagnostics = models.TextField(
        null=True,
        blank=True,
        help_text="Additional diagnostic information about the issue",
    )
    details = models.ForeignKey(
        Concept,
        null=True,
        blank=True,
        limit_choices_to={
            "valueset": Concept.VALUESET.UK_CORE_OPERATION_OUTCOME_ISSUE_DETAILS
        },
        on_delete=models.CASCADE,
        help_text="Additional details about the error",
    )
