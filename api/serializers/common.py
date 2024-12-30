from rest_framework.serializers import ModelSerializer


def is_none(obj) -> bool:
    if isinstance(obj, (bool, int, float)):
        return False
    return not obj


def strip_none(obj):
    if isinstance(obj, dict):
        return {k: strip_none(v) for k, v in obj.items() if not is_none(v)}
    if isinstance(obj, list):
        return list(map(strip_none, obj))
    return obj


class UKCoreModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return strip_none(representation)
