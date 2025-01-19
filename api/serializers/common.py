from datetime import datetime

from django.db.models import ForeignKey, OneToOneField
from django.utils.translation import gettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.fields import (
    CharField,
    DateTimeField,
    FloatField,
    IntegerField,
    SerializerMethodField,
    URLField,
)
from rest_framework.relations import RelatedField
from rest_framework.serializers import ModelSerializer, Serializer

from api.fields import PeriodField, QuantityField, TimingField
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


class FHIRDataTypeSerializer(Serializer):
    value = FloatField(required=False)
    code = CharField(required=False)
    system = URLField(required=False)
    unit = CharField(required=False)

    def __init__(self, *args, **kwargs):
        for key in "encoder", "decoder":
            kwargs.pop(key, None)
        super().__init__(*args, **kwargs)


class QuantitySerializer(FHIRDataTypeSerializer):
    value = FloatField(required=False)
    code = CharField(required=False)
    system = URLField(required=False)
    unit = CharField(required=False)


class TimingRepeatSerializer(FHIRDataTypeSerializer):
    frequency = IntegerField()
    period = IntegerField()
    periodUnit = CharField()


class TimingSerializer(FHIRDataTypeSerializer):
    repeat = TimingRepeatSerializer()


class PeriodSerializer(FHIRDataTypeSerializer):
    start = DateTimeField(required=False)
    end = DateTimeField(required=False)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        def f(x):
            if isinstance(x, datetime):
                return x.isoformat().replace("+00:00", "Z")
            return x

        return {k: f(v) for k, v in internal_value.items()}


class ConceptSerializer(Serializer):
    code = CharField()
    system = CharField(required=False)
    display = CharField(required=False)


class ConceptModelSerializer(RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid pk "{pk_value}" - object does not exist.'),
    }
    concept = ConceptSerializer()

    def to_internal_value(self, data):
        data = self.concept.to_internal_value(data)
        qs = self.get_queryset()
        try:
            return qs.get(code=data["code"])
        except Concept.DoesNotExist:
            self.fail("does_not_exist", pk_value=data["code"])

    def to_representation(self, instance):
        return self.concept.to_representation(instance)


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
        model_name = qs.model.__name__.removesuffix("Profile")
        if not isinstance(data, dict):
            self.fail("incorrect_type", type=dict)

        if model_name == "Concept":
            if not (isinstance(data, dict) and "coding" in data):
                self.fail("required")
            internal_value = self.coding.to_internal_value(data=data["coding"])
            code = internal_value[0]["code"]

            try:
                return qs.get(code=code)
            except Concept.DoesNotExist:
                self.fail("does_not_exist", pk_value=code)
        else:
            if not (isinstance(data, dict) and "reference" in data):
                self.fail("required")
            resource_type, id = data["reference"].split("/", 2)

            if field_name := self.source:
                parent = self.parent
            else:
                field_name = self.parent.field_name
                parent = self.parent.parent

            field = parent.Meta.model._meta.get_field(field_name)
            resource_types = field.remote_field.limit_choices_to.get(
                "polymorphic_ctype__model__in"
            )
            if (
                resource_types
                and resource_type.lower() + "profile" not in resource_types
            ):
                self.fail("incorrect_resource_type", resource_type=model_name)

            try:
                return qs.get(id=id)
            except qs.model.DoesNotExist:
                self.fail("does_not_exist", pk_value=id)

    def to_representation(self, value):
        model_name = value._meta.object_name.removesuffix("Profile")
        if model_name == "Concept":
            representation = self.coding.to_representation([value])
            return {"coding": representation}
        else:
            return {"reference": model_name + "/" + str(value.id)}


class BaseModelSerializer(WritableNestedModelSerializer):
    serializer_field_mapping = ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping[QuantityField] = QuantitySerializer
    serializer_field_mapping[TimingField] = TimingSerializer
    serializer_field_mapping[PeriodField] = PeriodSerializer

    serializer_related_field = RelatedResourceSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return strip_none(representation)

    def get_resourceType(self, _obj):
        return self.Meta.model.__name__.removesuffix("Profile")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_name = self.get_resourceType(None)

        for related_object in self.Meta.model._meta.related_objects:
            related_model = related_object.related_model

            field_name = related_model.__name__
            if this_name == field_name:
                continue

            if field_name.endswith("Profile"):
                continue

            field_name = field_name.removeprefix(this_name)
            field_name = field_name[0].lower() + field_name[1:]

            possible_fields = {
                field.attname
                for field in related_model._meta.concrete_fields
                if hasattr(field, "attname")
            }
            fields_to_exclude = {"uuid", "profile", "created_at", "updated_at"}

            class ChildSerializer(BaseModelSerializer):
                class Meta:
                    exclude = tuple(fields_to_exclude & possible_fields) + ("profile",)
                    model = related_model

            if field_name not in self.fields:
                if isinstance(related_object.field, OneToOneField):
                    self.fields[field_name] = ChildSerializer(
                        many=False,
                        required=False,
                        source=f"{this_name}{field_name}".lower(),
                    )
                elif isinstance(related_object.field, ForeignKey):
                    self.fields[field_name] = ChildSerializer(
                        many=True,
                        required=False,
                        source=f"{this_name}{field_name}_set".lower(),
                    )


class ProfileSerializer(BaseModelSerializer):
    id = CharField()
    resourceType = SerializerMethodField()
