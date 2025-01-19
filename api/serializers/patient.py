from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import RelatedField, Serializer

from api.models import PatientProfile
from api.models.datatypes import Concept
from api.serializers.common import (
    ConceptSerializer,
    ProfileSerializer,
)


class LanguageSerializer(Serializer):
    coding = ConceptSerializer(many=True)


class PatientCommunicationSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_format": _(
            'Incorrect format. Expected {"language": {"coding": [{"code": code]}}.'
        ),
    }

    def to_internal_value(self, data):
        try:
            code = data["language"]["coding"][0]["code"]
        except (KeyError, IndexError):
            self.fail("incorrect_format")

        try:
            return self.get_queryset().get(code=code)
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=code)

    def to_representation(self, value):
        return {
            "language": {
                "coding": [
                    {
                        "code": value.code,
                        "system": value.system,
                        "display": value.display,
                    }
                ]
            }
        }


class PatientSerializer(ProfileSerializer):
    communication = PatientCommunicationSerializer(
        required=False,
        many=True,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_HUMAN_LANGUAGE
        ),
    )

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = PatientProfile
