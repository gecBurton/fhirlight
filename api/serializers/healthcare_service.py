from api.models import HealthcareServiceProfile
from api.serializers.common import ProfileSerializer


class HealthcareServiceSerializer(ProfileSerializer):
    class Meta:
        exclude = ("created_at", "polymorphic_ctype", "updated_at")
        model = HealthcareServiceProfile
