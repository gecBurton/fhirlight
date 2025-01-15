from django.core.exceptions import ValidationError
from django.db.models import JSONField


class FHIRDataTypeField(JSONField):
    types: dict

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        if not isinstance(value, dict):
            raise ValidationError("Quantity must be a dict")

        for field_name, field_type in self.types.items():
            if field_name not in self.types:
                raise ValidationError(f"field {field_name} is not expected")
            if field_name in value and not isinstance(value[field_name], field_type):
                raise ValidationError(
                    f"expected {field_name}={value[field_name]} to have type {field_type}"
                )


class QuantityField(JSONField):
    description = "https://build.fhir.org/datatypes.html#Quantity"
    types = {"value": (int, float), "code": str, "unit": str, "system": str}


class TimingField(FHIRDataTypeField):
    description = "https://build.fhir.org/datatypes.html#timing"
    types = {"repeat": dict}
