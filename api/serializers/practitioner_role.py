from api.models import PractitionerRoleProfile
from api.serializers.common import (
    ProfileSerializer,
)


class PractitionerRoleSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = PractitionerRoleProfile
