from api.models import PractitionerRoleProfile
from api.models.practitioner_role import (
    PractitionerRoleIdentifier,
    PractitionerRoleTelecom,
)
from api.serializers.common import (
    ProfileSerializer,
    BaseModelSerializer,
)


class PractitionerRoleIdentifierSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner_role", "created_at", "updated_at")
        model = PractitionerRoleIdentifier


class PractitionerRoleTelecomSerializer(BaseModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner_role", "created_at", "updated_at")
        model = PractitionerRoleTelecom


class PractitionerRoleSerializer(ProfileSerializer):
    identifier = PractitionerRoleIdentifierSerializer(
        many=True, required=False, source="practitionerroleidentifier_set"
    )
    telecom = PractitionerRoleTelecomSerializer(
        many=True, required=False, source="practitionerroletelecom_set"
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "telecom",
            "organization",
            "practitioner",
            "code",
            "specialty",
        )
        model = PractitionerRoleProfile
