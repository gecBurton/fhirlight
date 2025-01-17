from rest_framework.fields import (
    BooleanField,
)
from rest_framework.serializers import Serializer

from api.models import MedicationRequestProfile
from api.serializers.common import (
    ProfileSerializer,
)


class SubstitutionSerializer(Serializer):
    allowedBoolean = BooleanField(required=False, source="substitutionAllowedBoolean")


class MedicationRequestSerializer(ProfileSerializer):
    substitution = SubstitutionSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "substitutionAllowedBoolean",
        )
        model = MedicationRequestProfile
