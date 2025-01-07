from rest_framework.fields import IntegerField, CharField, URLField
from rest_framework.serializers import Serializer

from api.models import FamilyMemberHistoryProfile
from api.models.family_member_history import FamilyMemberHistoryCondition
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class FamilyMemberHistoryConditionOnsetSerializer(Serializer):
    value = IntegerField(required=False, source="onsetAgeValue")
    unit = CharField(required=False, source="onsetAgeUnit")
    system = URLField(required=False, source="onsetAgeSystem")
    code = CharField(required=False, source="onsetAgeCode")


class FamilyMemberHistoryConditionSerializer(BaseModelSerializer):
    onsetAge = FamilyMemberHistoryConditionOnsetSerializer(required=False, source="*")

    class Meta:
        fields = ("code", "onsetAge")
        model = FamilyMemberHistoryCondition


class FamilyMemberHistorySerializer(ProfileSerializer):
    condition = FamilyMemberHistoryConditionSerializer(
        many=True, required=False, source="familymemberhistorycondition_set"
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "status",
            "patient",
            "date",
            "bornDate",
            "relationship",
            "sex",
            "name",
            "condition",
        )
        model = FamilyMemberHistoryProfile
