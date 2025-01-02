from rest_framework.fields import DateTimeField
from rest_framework.serializers import Serializer, ModelSerializer

from api.models import Questionnaire
from api.models.questionnaire import QuestionnaireIdentifier, QuestionnaireContactPoint
from api.serializers.common import UKCoreProfileSerializer, UKCoreModelSerializer


class QuestionnaireIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "questionnaire", "created_at", "updated_at")
        model = QuestionnaireIdentifier


class QuestionnaireContactDetailSerializer(ModelSerializer):
    def to_internal_value(self, data):
        _data = data["telecom"][0]
        _data["name"] = data["name"]
        return super().to_internal_value(_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {"telecom": [representation], "name": instance.get("name")}

    class Meta:
        exclude = ("uuid", "questionnaire", "created_at", "updated_at")
        model = QuestionnaireContactPoint


class effectivePeriodSerializer(Serializer):
    start = DateTimeField(required=False, source="effectivePeriodStart")
    end = DateTimeField(required=False, source="effectivePeriodEnd")


class QuestionnaireSerializer(UKCoreProfileSerializer):
    effectivePeriod = effectivePeriodSerializer(required=False, source="*")
    identifier = QuestionnaireIdentifierSerializer(many=True, required=False)
    contact = QuestionnaireContactDetailSerializer(required=False, many=True)

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "url",
            "contact",
            "status",
            "title",
            "experimental",
            "date",
            "publisher",
            "purpose",
            "subjectType",
            "effectivePeriod",
        )
        model = Questionnaire
