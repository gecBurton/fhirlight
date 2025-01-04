from api.models.operation_outcome import OperationOutcomeProfile, OperationOutcomeIssue
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class OperationOutcomeIssueSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "operation_outcome", "created_at", "updated_at")
        model = OperationOutcomeIssue


class OperationOutcomeSerializer(ProfileSerializer):
    issue = OperationOutcomeIssueSerializer(
        many=True, source="operationoutcomeissue_set"
    )

    class Meta:
        fields = ("id", "resourceType", "issue")
        model = OperationOutcomeProfile
