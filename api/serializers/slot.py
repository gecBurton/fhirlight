from api.models.datatypes import Concept
from api.models.slot import Slot, SlotIdentifier
from api.serializers.common import (
    UKCoreProfileSerializer,
    CodingSerializer,
    UKCoreModelSerializer,
)


class SlotIdentifierSerializer(UKCoreModelSerializer):
    class Meta:
        exclude = ("uuid", "slot", "created_at", "updated_at")
        model = SlotIdentifier


class SlotSerializer(UKCoreProfileSerializer):
    identifier = SlotIdentifierSerializer(
        many=True, required=False, source="slotidentifier_set"
    )

    serviceCategory = CodingSerializer(
        required=False,
        many=True,
        valueset=Concept.VALUESET.SERVICE_CATEGORY,
    )
    serviceType = CodingSerializer(
        required=False,
        many=True,
        valueset=Concept.VALUESET.SERVICE_TYPE,
    )
    specialty = CodingSerializer(
        required=False,
        many=True,
        valueset=Concept.VALUESET.UK_CORE_PRACTICE_SETTINGS_CODE,
    )
    appointmentType = CodingSerializer(
        required=False,
        valueset=Concept.VALUESET.V2_0276,
    )

    class Meta:
        fields = (
            "id",
            "resourceType",
            "identifier",
            "comment",
            "serviceCategory",
            "serviceType",
            "specialty",
            "appointmentType",
            "start",
            "end",
            "status",
        )
        model = Slot
