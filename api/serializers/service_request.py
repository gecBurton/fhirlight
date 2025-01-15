from api.models.service_request import ServiceRequestProfile
from api.serializers.common import ProfileSerializer


class ServiceRequestSerializer(ProfileSerializer):
    class Meta:
        exclude = (
            "created_at",
            "updated_at",
            "polymorphic_ctype",
        )
        model = ServiceRequestProfile
