from api.models.consent import ConsentProfile, ConsentPolicy
from api.models.datatypes import Concept
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
    ConceptModelSerializer,
)


class ConsentPolicySerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "consent", "created_at", "updated_at")
        model = ConsentPolicy


class ConsentProvisionSerializer(ProfileSerializer):
    purpose = ConceptModelSerializer(
        many=True,
        required=False,
        source="provisionPurpose",
        queryset=Concept.objects.filter(valueset=Concept.VALUESET.V3_PURPOSE_OF_USE),
    )

    class Meta:
        fields = ("purpose",)
        model = ConsentProfile


class ConsentSerializer(ProfileSerializer):
    policy = ConsentPolicySerializer(
        required=False, many=True, source="consentpolicy_set"
    )
    provision = ConsentProvisionSerializer(required=False, source="*")

    class Meta:
        fields = (
            "id",
            "resourceType",
            "status",
            "dateTime",
            "scope",
            "category",
            "patient",
            "performer",
            "organization",
            "provision",
            "policy",
        )
        model = ConsentProfile
