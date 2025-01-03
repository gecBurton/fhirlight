from api.models import PractitionerRole
from api.models.datatypes import Concept
from api.models.practitioner_role import (
    PractitionerRoleIdentifier,
    PractitionerRoleTelecom,
)
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
    CodingSerializer,
)


class PractitionerRoleIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner_role", "created_at", "updated_at")
        model = PractitionerRoleIdentifier


class PractitionerRoleTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "practitioner_role", "created_at", "updated_at")
        model = PractitionerRoleTelecom


class PractitionerRoleSerializer(UKCoreProfileSerializer):
    code = CodingSerializer(
        many=True, required=False, valueset=Concept.VALUESET.PRACTITIONER_ROLE
    )
    specialty = CodingSerializer(
        many=True,
        required=False,
        valueset=Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE,
    )
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
        model = PractitionerRole
