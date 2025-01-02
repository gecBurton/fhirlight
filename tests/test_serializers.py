import copy
import json
import os

import pytest

from api.serializers.immunization import ImmunizationSerializer
from api.serializers.location import LocationSerializer
from api.serializers.medication import MedicationSerializer
from api.serializers.observation import ObservationSerializer
from api.serializers.operation_outcome import OperationOutcomeSerializer
from api.serializers.organization import OrganizationSerializer
from api.serializers.patient import PatientSerializer
from api.serializers.practitioner import PractitionerSerializer
from api.serializers.practitioner_role import PractitionerRoleSerializer
from api.serializers.questionnaire import QuestionnaireSerializer
from api.serializers.schedule import ScheduleSerializer
from api.serializers.slot import SlotSerializer
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
        "UKCore-Observation-VitalSigns-BloodPressure-Example",
        "UKCore-Observation-VitalSigns-BMI-Example",
        "UKCore-Observation-VitalSigns-BodyHeight-Example",
        "UKCore-Observation-VitalSigns-BodyTemperature-Example",
        "UKCore-Observation-VitalSigns-BodyWeight-Example",
        "UKCore-Observation-VitalSigns-HeadCircumference-Example",
        "UKCore-Observation-VitalSigns-HeartRate-Example",
        "UKCore-Observation-VitalSigns-OxygenSaturation-Example",
        "UKCore-Observation-VitalSigns-RespiratoryRate-Example",
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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Location-GeneralPracticeNurseClinic-Example",
        "UKCore-Location-CardiologySJUH-Example",
        "UKCore-Location-HospitalSJUH-Example",
    ],
)
def test_location(resource, leeds_teaching_hospital, white_rose_medical_centre):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = LocationSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Immunization-InfluenzaVaccine-Example",
    ],
)
def test_immunization(resource, general_practice_nurse_clinic, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ImmunizationSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-OperationOutcome-DateError-Example",
    ],
)
def test_operation_outcome(resource, general_practice_nurse_clinic, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = OperationOutcomeSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Slot-AvailableWalkInVisit-Example",
    ],
)
def test_slot(resource, general_practice_nurse_clinic, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = SlotSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-PractitionerRole-GeneralPractitioner-Example",
    ],
)
def test_practitioner_role(resource, white_rose_medical_centre, doctor_paul_rastall):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = PractitionerRoleSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Schedule-Immunization-Example",
    ],
)
def test_schedule(resource, general_practice_nurse_clinic):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ScheduleSerializer(data=payload)
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Questionnaire-InpatientSurvey-Example",
    ],
)
def test_questionnaire(resource, general_practice_nurse_clinic):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = QuestionnaireSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload
