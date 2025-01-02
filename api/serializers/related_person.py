from api.models import Patient, RelatedPerson
from api.models.datatypes import Concept
from api.models.related_person import (
    RelatedPersonAddress,
    RelatedPersonTelecom,
    RelatedPersonName,
)
from api.serializers.common import (
    UKCoreProfileSerializer,
    RelatedResourceSerializer,
    CodingSerializer,
    UKCoreModelSerializer,
)


class RelatedPersonAddressSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "related_person", "created_at", "updated_at")
        model = RelatedPersonAddress


class RelatedPersonTelecomSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "related_person", "created_at", "updated_at")
        model = RelatedPersonTelecom


class RelatedPersonNameSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "related_person", "created_at", "updated_at")
        model = RelatedPersonName


class RelatedPersonSerializer(UKCoreProfileSerializer):
    name = RelatedPersonNameSerializer(
        required=False, many=True, source="relatedpersonname_set"
    )
    telecom = RelatedPersonTelecomSerializer(required=False, many=True)
    address = RelatedPersonAddressSerializer(required=False, many=True)

    patient = RelatedResourceSerializer(queryset=Patient.objects.all())
    relationship = CodingSerializer(
        many=True,
        required=False,
        valueset=Concept.VALUESET.UK_CORE_PERSON_RELATIONSHIP_TYPE,
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "patient",
            "relationship",
            "name",
            "telecom",
            "address",
        )
        model = RelatedPerson
