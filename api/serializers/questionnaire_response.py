from api.models.questionnaire_response import (
    QuestionnaireResponseItem,
    QuestionnaireResponseProfile,
)
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class QuestionnaireResponseChildItemSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "parent", "created_at", "updated_at")
        model = QuestionnaireResponseItem


class QuestionnaireResponseItemSerializer(QuestionnaireResponseChildItemSerializer):
    """allows for 1 level of recursion"""

    item = QuestionnaireResponseChildItemSerializer(
        many=True, required=False, source="questionnaireresponseitem_set"
    )


class QuestionnaireResponseSerializer(ProfileSerializer):
    item = QuestionnaireResponseItemSerializer(
        many=True, required=False, source="questionnaireresponseitem_set"
    )

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = QuestionnaireResponseProfile
