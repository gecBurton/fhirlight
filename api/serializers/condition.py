from api.models import ConditionProfile
from api.serializers.common import ProfileSerializer


class ConditionSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = ConditionProfile
