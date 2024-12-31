from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _

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
    return obj


class UKCoreModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return strip_none(representation)


class ConceptSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_format": _(
            'Incorrect format. Expected {"language": {"coding": [{"code": code]}}.'
        ),
    }

    def to_internal_value(self, data):
        try:
            code = data["coding"][0]["code"]
        except (KeyError, IndexError):
            self.fail("incorrect_format")

        try:
            return self.get_queryset().get(code=code)
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=code)

    def to_representation(self, value):
        return {
            "coding": [
                {
                    "code": value.code,
                    "system": value.system,
                    "display": value.display,
                }
            ]
        }


class RelatedResourceSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
        "incorrect_format": _(
            'Incorrect format. Expected {"language": {"coding": [{"code": code]}}.'
        ),
    }

    def to_internal_value(self, data):
        qs = self.get_queryset()
        resource_type, id = data["reference"].split("/", 2)
        assert resource_type == qs.model.__name__
        try:
            return qs.get(id=id)
        except qs.model.DoesNotExist:
            self.fail("does_not_exist", pk_value=id)

    def to_representation(self, value):
        qs = self.get_queryset()
        return {"reference": qs.model.__name__ + "/" + value.id}
