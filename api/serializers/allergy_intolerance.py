from api.models import AllergyIntoleranceProfile
from api.serializers.common import ProfileSerializer


class AllergyIntoleranceSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "updated_at", "polymorphic_ctype")
        model = AllergyIntoleranceProfile
