import json
import os

import pytest

from api.serializers.medication import MedicationSerializer
from api.serializers.observation import ObservationSerializer
from api.serializers.organization import OrganizationSerializer
from api.serializers.patient import PatientSerializer
from api.serializers.practitioner import PractitionerSerializer
from api.serializers.specimen import SpecimenSerializer

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Organization-LeedsTeachingHospital-Example",
        "UKCore-Organization-WhiteRoseMedicalCentre-Example",
    ],
)
def test_organizations(resource):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = OrganizationSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Practitioner-ConsultantSandraGose-Example",
        "UKCore-Practitioner-DoctorPaulRastall-Example",
        "UKCore-Practitioner-PharmacistJimmyChuck-Example",
    ],
)
def test_practitioner(resource):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = PractitionerSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Patient-BabyPatient-Example",
        "UKCore-Patient-RichardSmith-Example",
    ],
)
def test_patient(resource):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = PatientSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Medication-COVID-Vaccine-Example",
        "UKCore-Medication-TimololVTM-Example",
        "UKCore-Medication-TimoptolEyeDrops-Example",
    ],
)
def test_medication(resource):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = MedicationSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Observation-24HourBloodPressure-Example",
        "UKCore-Observation-AwarenessOfDiagnosis-Example",
        "UKCore-Observation-BreathingNormally-Example",
        "UKCore-Observation-DrugUse-Example",
        "UKCore-Observation-FastingTest-Example",
        # "UKCore-Observation-FingerJointInflamed-Example",performer=Practitioner
        "UKCore-Observation-Group-FullBloodCount-Example",
        "UKCore-Observation-HeavyDrinker-Example",
        # "UKCore-Observation-Lab-RedCellCount-Example", missing referenceRange and specimen
        # "UKCore-Observation-Lab-WhiteCellCount-Example",missing referenceRange and specimen
    ],
)
def test_observation(
    resource, richard_smith, leeds_teaching_hospital, white_cell_count, red_cell_count
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ObservationSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    ["UKCore-Specimen-UrineSpecimen-Example", "UKCore-Specimen-BloodSpecimen-Example"],
)
def test_specimen(resource, richard_smith, consultant_sandra_gose):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = SpecimenSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload
