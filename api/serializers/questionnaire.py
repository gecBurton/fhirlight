from rest_framework.serializers import ModelSerializer

from api.models import QuestionnaireProfile
from api.models.questionnaire import (
    QuestionnaireIdentifier,
    QuestionnaireContact,
    QuestionnaireItem,
)
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class QuestionnaireIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = QuestionnaireIdentifier


class QuestionnaireChildItemSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "parent", "created_at", "updated_at")
        model = QuestionnaireItem


class QuestionnaireItemSerializer(QuestionnaireChildItemSerializer):
    """allows for 1 level of recursion"""

    item = QuestionnaireChildItemSerializer(
        many=True, required=False, source="questionnaireitem_set"
    )


class QuestionnaireTelecomSerializer(ModelSerializer):
    def to_internal_value(self, data):
        _data = data["telecom"][0]
        _data["name"] = data["name"]
        return super().to_internal_value(_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {"telecom": [representation], "name": representation.pop("name", None)}

    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = QuestionnaireContact


class QuestionnaireSerializer(ProfileSerializer):
    identifier = QuestionnaireIdentifierSerializer(
        many=True, required=False, source="questionnaireidentifier_set"
    )
    contact = QuestionnaireTelecomSerializer(
        required=False, many=True, source="questionnairecontact_set"
    )
    item = QuestionnaireItemSerializer(
        many=True, required=False, source="questionnaireitem_set"
    )

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = QuestionnaireProfile
