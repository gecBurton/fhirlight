import json
import os

import pytest

from api.serializers.organization import OrganizationSerializer
from api.serializers.practitioner import PractitionerSerializer

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "organization",
    [
        "UKCore-Organization-LeedsTeachingHospital-Example",
        "UKCore-Organization-WhiteRoseMedicalCentre-Example",
    ],
)
def test_organizations(organization):
    with open(f"{TEST_DIR}/data/{organization}.json") as f:
        payload = json.load(f)

    serializer = OrganizationSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "practitioner",
    [
        "UKCore-Practitioner-ConsultantSandraGose-Example",
        "UKCore-Practitioner-DoctorPaulRastall-Example",
        "UKCore-Practitioner-PharmacistJimmyChuck-Example",
    ],
)
def test_practitioner(practitioner):
    with open(f"{TEST_DIR}/data/{practitioner}.json") as f:
        payload = json.load(f)

    serializer = PractitionerSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload
