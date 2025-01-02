from api.models import PractitionerRole, Organization, Practitioner
from api.models.datatypes import Concept
from api.models.practitioner_role import (
    PractitionerRoleIdentifier,
    PractitionerRoleTelecom,
)
from api.serializers.common import (
    UKCoreProfileSerializer,
    UKCoreModelSerializer,
    RelatedResourceSerializer,
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
    organization = RelatedResourceSerializer(queryset=Organization.objects.all())
    practitioner = RelatedResourceSerializer(queryset=Practitioner.objects.all())
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
