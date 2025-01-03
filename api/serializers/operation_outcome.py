from api.models.operation_outcome import UKCoreOperationOutcome, OperationOutcomeIssue
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
)


class OperationOutcomeIssueSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "operation_outcome", "created_at", "updated_at")
        model = OperationOutcomeIssue


class OperationOutcomeSerializer(UKCoreProfileSerializer):
    issue = OperationOutcomeIssueSerializer(
        many=True, source="operationoutcomeissue_set"
    )

    class Meta:
        fields = ("id", "resourceType", "issue")
        model = UKCoreOperationOutcome
