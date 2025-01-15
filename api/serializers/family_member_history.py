from api.models import FamilyMemberHistoryProfile
from api.models.family_member_history import FamilyMemberHistoryCondition
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class FamilyMemberHistoryConditionSerializer(BaseModelSerializer):
    class Meta:
        fields = ("code", "onsetAge")
        model = FamilyMemberHistoryCondition


class FamilyMemberHistorySerializer(ProfileSerializer):
    condition = FamilyMemberHistoryConditionSerializer(
        many=True, required=False, source="familymemberhistorycondition_set"
    )

    class Meta:
        exclude = ["created_at", "updated_at", "polymorphic_ctype"]
        model = FamilyMemberHistoryProfile
