from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer

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


class effectivePeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="effectivePeriodStart")
    end = DateTimeField(required=False, source="effectivePeriodEnd")


class QuestionnaireResponseSerializer(ProfileSerializer):
    effectivePeriod = effectivePeriodSerializer(required=False, source="*")
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
