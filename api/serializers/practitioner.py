from api.models import (
    PractitionerProfile,
)
from api.serializers.common import ProfileSerializer


class PractitionerSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = PractitionerProfile
