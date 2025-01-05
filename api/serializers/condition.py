from api.models import ConditionProfile
from api.serializers.common import ProfileSerializer


class ConditionSerializer(ProfileSerializer):
    class Meta:
        fields = (
            "id",
            "resourceType",
            "clinicalStatus",
            "verificationStatus",
            "category",
            "severity",
            "code",
            "subject",
            "recorder",
        )
        model = ConditionProfile
