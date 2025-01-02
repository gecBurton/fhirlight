from api.models import Questionnaire, Patient, Practitioner
from api.serializers.common import RelatedResourceSerializer
from api.serializers.questionnaire import (
    QuestionnaireSerializer,
    QuestionnaireIdentifierSerializer,
)


class QuestionnaireResponseSerializer(QuestionnaireSerializer):
    identifier = QuestionnaireIdentifierSerializer(
        required=False, source="questionnaireidentifier_set"
    )
    subject = RelatedResourceSerializer(required=False, queryset=Patient.objects.all())
    author = RelatedResourceSerializer(
        required=False, queryset=Practitioner.objects.all()
    )

    def get_resourceType(self, _obj):
        return "QuestionnaireResponse"

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
            "item",
            "subject",
            "author",
            "authored",
        )
        model = Questionnaire
