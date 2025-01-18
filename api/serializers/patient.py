from rest_framework.fields import DateTimeField, CharField, JSONField, BooleanField
from rest_framework.serializers import Serializer, RelatedField, SerializerMethodField

from api.models import PatientProfile
from api.models.datatypes import Concept
from api.models.patient import PatientExtension, PatientContact
from api.serializers.common import (
    ProfileSerializer,
    ConceptSerializer,
    BaseModelSerializer,
    TimingSerializer,
)

from django.utils.translation import gettext_lazy as _


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


class BirthDateExtensionSerializer(Serializer):
    valueDateTime = DateTimeField(required=False)
    url = SerializerMethodField(read_only=True)

    def get_url(self, _):
        return "http://hl7.org/fhir/StructureDefinition/patient-birthTime"


class BirthDateSerializer(Serializer):
    extension = BirthDateExtensionSerializer(many=True)

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        return internal_data["extension"][0]["valueDateTime"]

    def to_representation(self, instance):
        return super().to_representation({"extension": [{"valueDateTime": instance}]})


class BaseExtensionSerializer(BaseModelSerializer):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
    }

    url = CharField()
    valueAddress = JSONField(required=False)
    valueBoolean = BooleanField(required=False)
    valueCodeableConcept = JSONField(required=False)
    valueDateTime = DateTimeField(required=False)
    valueTiming = TimingSerializer(required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        if valueCodeableConcept := data.get("valueCodeableConcept"):
            code = valueCodeableConcept["coding"][0]["code"]
            url = data["url"]
            valuesets = {
                "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-EthnicCategory": Concept.VALUESET.UK_CORE_ETHNIC_CATEGORY,
                "PreferredContactMethod": Concept.VALUESET.UK_CORE_PREFERRED_CONTACT_METHOD,
                "PreferredWrittenCommunicationFormat": Concept.VALUESET.UK_CORE_PREFERRED_WRITTEN_COMMUNICATION_FORMAT,
                "deathNotificationStatus": Concept.VALUESET.UK_CORE_DEATH_NOTIFICATION_STATUS,
                "https://fhir.hl7.org.uk/StructureDefinition/Extension-UKCore-ResidentialStatus": Concept.VALUESET.UK_CORE_RESIDENTIAL_STATUS,
            }
            valueset = valuesets[url]
            try:
                internal_value["valueCodeableConcept"] = Concept.objects.get(
                    code=code, valueset=valueset
                )
            except Concept.DoesNotExist:
                self.fail("does_not_exist", pk_value=(code, valueset))
        return internal_value

    def to_representation(self, instance):
        if isinstance(instance, dict):
            if valueCodeableConcept := instance.get("valueCodeableConcept"):
                instance["valueCodeableConcept"] = {
                    "coding": [
                        {
                            "code": valueCodeableConcept.code,
                            "system": valueCodeableConcept.system,
                            "display": valueCodeableConcept.display,
                        }
                    ]
                }
        return super().to_representation(instance)

    # extension = models.ManyToManyField("self", blank=True)
    class Meta:
        exclude = ("created_at", "updated_at", "profile")
        model = PatientExtension


class ExtensionSerializer(BaseExtensionSerializer):
    extension = BaseExtensionSerializer(many=True, required=False)


class PatientContactSerializer(BaseModelSerializer):
    extension = ExtensionSerializer(many=True, required=False)

    class Meta:
        exclude = ("uuid", "created_at", "updated_at", "profile")
        model = PatientContact


class PatientSerializer(ProfileSerializer):
    extension = ExtensionSerializer(
        many=True, required=False, source="patientextension_set"
    )
    communication = PatientCommunicationSerializer(
        required=False,
        many=True,
        queryset=Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_HUMAN_LANGUAGE
        ),
    )

    _birthDate = BirthDateSerializer(required=False)

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = PatientProfile
