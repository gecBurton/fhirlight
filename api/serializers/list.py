from api.models.list import ListProfile
from api.serializers.common import ProfileSerializer


class ListSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "active",
            "updated_at",
            "polymorphic_ctype",
        )
        model = ListProfile
