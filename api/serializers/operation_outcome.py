from api.models.datatypes import Concept
from api.models.operation_outcome import OperationOutcome, OperationOutcomeIssue
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
    CodingSerializer,
)


class OperationOutcomeIssueSerializer(UKCoreModelSerializer):
    details = CodingSerializer(
        required=False,
        valueset=Concept.VALUESET.UK_CORE_OPERATION_OUTCOME_ISSUE_DETAILS,
    )

    class Meta:
        exclude = ("uuid", "operation_outcome", "created_at", "updated_at")
        model = OperationOutcomeIssue


class OperationOutcomeSerializer(UKCoreProfileSerializer):
    issue = OperationOutcomeIssueSerializer(
        many=True, source="operationoutcomeissue_set"
    )

    class Meta:
        fields = ("id", "resourceType", "issue")
        model = OperationOutcome
