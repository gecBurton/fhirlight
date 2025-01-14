from rest_framework.serializers import Serializer

from api.models.consent import ConsentProfile
from api.models.datatypes import Concept
from api.serializers.common import (
    ProfileSerializer,
    ConceptModelSerializer,
)


class ConsentProvisionSerializer(Serializer):
    purpose = ConceptModelSerializer(
        many=True,
        required=False,
        source="provisionPurpose",
        queryset=Concept.objects.filter(valueset=Concept.VALUESET.V3_PURPOSE_OF_USE),
    )


class ConsentSerializer(ProfileSerializer):
    provision = ConsentProvisionSerializer(required=False, source="*")

    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
            "provisionPurpose",
        )
        model = ConsentProfile
