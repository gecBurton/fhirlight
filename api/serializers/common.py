from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.relations import RelatedField
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import Serializer

from api.models.datatypes import Concept


def is_none(obj) -> bool:
    if isinstance(obj, (bool, int, float)):
        return False
    if isinstance(obj, dict):
        if all(map(is_none, obj.values())):
            return True
    return not obj


def strip_none(obj):
    if isinstance(obj, dict):
        return {k: strip_none(v) for k, v in obj.items() if not is_none(v)}
    if isinstance(obj, list):
        return list(map(strip_none, obj))

    if isinstance(obj, str):
        return obj.removesuffix("T00:00:00Z")

    if isinstance(obj, str):
        if obj.endswith(":00Z"):
            return obj.replace(":00Z", "00+00:00")
    return obj


class UKCoreModelSerializer(WritableNestedModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return strip_none(representation)


class UKCoreProfileSerializer(UKCoreModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()

    def get_resourceType(self, _obj):
        return self.Meta.model.__name__


class ConceptSerializer(Serializer):
    code = CharField()
    system = CharField(required=False)
    display = CharField(required=False)


class CodingSerializerSimple(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
    }
    coding = ConceptSerializer()

    def to_internal_value(self, data):
        try:
            internal_value = self.coding.to_internal_value(data=data)
        except Exception:
            raise
        code = internal_value["code"]

        try:
            return self.get_queryset().get(code=code)
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=code)

    def to_representation(self, value):
        representation = self.coding.to_representation(value)
        return representation


class CodingSerializer(RelatedField):
    coding = ConceptSerializer(many=True)
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
    }

    def __init__(self, valueset: str, many: bool = False, required: bool = True):
        queryset = Concept.objects.filter(valueset=valueset)
        super().__init__(queryset=queryset, many=many, required=required)

    def to_internal_value(self, data):
        if not (isinstance(data, dict) and "coding" in data):
            self.fail("required")
        internal_value = self.coding.to_internal_value(data=data["coding"])
        code = internal_value[0]["code"]

        try:
            return self.get_queryset().get(code=code)
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=code)

    def to_representation(self, value):
        representation = self.coding.to_representation([value])
        return {"coding": representation}


class RelatedResourceSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_format": _(
            'Incorrect format. Expected {"language": {"coding": [{"code": code]}}.'
        ),
        "incorrect_resource_type": _(
            "incorrect resourceType. Expected {resource_type}"
        ),
        "incorrect_type": _("incorrect type. Expected {type}"),
    }

    def to_internal_value(self, data):
        qs = self.get_queryset()
        if not isinstance(data, dict):
            self.fail("incorrect_type", type=dict)
        resource_type, id = data["reference"].split("/", 2)
        if resource_type != qs.model.__name__:
            self.fail("incorrect_resource_type", resource_type=qs.model.__name__)
        try:
            return qs.get(id=id)
        except qs.model.DoesNotExist:
            self.fail("does_not_exist", pk_value=id)

    def to_representation(self, value):
        qs = self.get_queryset()
        return {"reference": qs.model.__name__ + "/" + value.id}
