from api.models import AllergyIntoleranceProfile
from api.models.allergy_intolerance import AllergyIntoleranceReaction
from api.serializers.common import ProfileSerializer, BaseModelSerializer


class AllergyIntoleranceReactionSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "profile", "created_at", "updated_at")
        model = AllergyIntoleranceReaction


class AllergyIntoleranceSerializer(ProfileSerializer):
    reaction = AllergyIntoleranceReactionSerializer(
        many=True, required=False, source="allergyintolerancereaction_set"
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "reaction",
            "clinicalStatus",
            "code",
            "verificationStatus",
            "patient",
            "encounter",
            "recorder",
            "asserter",
            "recordedDate",
        )
        model = AllergyIntoleranceProfile
