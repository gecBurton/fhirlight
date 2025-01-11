from api.models import RelatedPersonProfile
from api.serializers.common import (
    ProfileSerializer,
)


class RelatedPersonSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype", "active")
        model = RelatedPersonProfile
