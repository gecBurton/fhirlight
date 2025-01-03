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


class ConceptSerializer(Serializer):
    code = CharField()
    system = CharField(required=False)
    display = CharField(required=False)


class RelatedResourceSerializer(RelatedField):
    coding = ConceptSerializer(many=True)

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

        if qs.model.__name__ == "Concept":
            if not (isinstance(data, dict) and "coding" in data):
                self.fail("required")
            try:
                internal_value = self.coding.to_internal_value(data=data["coding"])
            except Exception:
                raise
            code = internal_value[0]["code"]

            try:
                return qs.get(code=code)
            except Concept.DoesNotExist:
                self.fail("does_not_exist", pk_value=code)
        else:
            resource_type, id = data["reference"].split("/", 2)
            if resource_type != qs.model.__name__:
                self.fail("incorrect_resource_type", resource_type=qs.model.__name__)
            try:
                return qs.get(id=id)
            except qs.model.DoesNotExist:
                self.fail("does_not_exist", pk_value=id)

    def to_representation(self, value):
        qs = self.get_queryset()
        model_name = qs.model.__name__
        if model_name == "Concept":
            representation = self.coding.to_representation([value])
            return {"coding": representation}
        else:
            return {"reference": model_name + "/" + value.id}


class UKCoreModelSerializer(WritableNestedModelSerializer):
    serializer_related_field = RelatedResourceSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return strip_none(representation)


class UKCoreProfileSerializer(UKCoreModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()

    def get_resourceType(self, _obj):
        return self.Meta.model.__name__
