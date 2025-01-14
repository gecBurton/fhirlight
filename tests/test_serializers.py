import copy
import json
import os

import pytest

from api.serializers import (
    ServiceRequestSerializer,
    AllergyIntoleranceSerializer,
    AppointmentSerializer,
    CompositionSerializer,
    MedicationRequestSerializer,
    MedicationAdministrationSerializer,
    MedicationStatementSerializer,
)
from api.serializers.condition import ConditionSerializer
from api.serializers.consent import ConsentSerializer
from api.serializers.device import DeviceSerializer
from api.serializers.diagnostic_report import DiagnosticReportSerializer
from api.serializers.encounter import EncounterSerializer
from api.serializers.episode_of_care import EpisodeOfCareSerializer
from api.serializers.family_member_history import FamilyMemberHistorySerializer
from api.serializers.flag import FlagSerializer
from api.serializers.healthcare_service import HealthcareServiceSerializer
from api.serializers.imaging_study import ImagingStudySerializer
from api.serializers.immunization import ImmunizationSerializer
from api.serializers.list import ListSerializer
from api.serializers.location import LocationSerializer
from api.serializers.medication import MedicationSerializer
from api.serializers.medication_dispense import MedicationDispenseSerializer
from api.serializers.message_header import MessageHeaderSerializer
from api.serializers.observation import ObservationSerializer
from api.serializers.operation_outcome import OperationOutcomeSerializer
from api.serializers.organization import OrganizationSerializer
from api.serializers.patient import PatientSerializer
from api.serializers.practitioner import PractitionerSerializer
from api.serializers.practitioner_role import PractitionerRoleSerializer
from api.serializers.procedure import ProcedureSerializer
from api.serializers.questionnaire import QuestionnaireSerializer
from api.serializers.questionnaire_response import QuestionnaireResponseSerializer
from api.serializers.related_person import RelatedPersonSerializer
from api.serializers.schedule import ScheduleSerializer
from api.serializers.slot import SlotSerializer
from api.serializers.specimen import SpecimenSerializer
from api.serializers.task import TaskSerializer

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Organization-LeedsTeachingHospital-Example",
        "UKCore-Organization-WhiteRoseMedicalCentre-Example",
        "UKCore-Organization-Maximal-Example",
    ],
)
def test_organizations(resource, minimal_organization):
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
        "UKCore-Observation-FingerJointInflamed-Example",
        "UKCore-Observation-Group-FullBloodCount-Example",
        "UKCore-Observation-HeavyDrinker-Example",
        "UKCore-Observation-Lab-RedCellCount-Example",
        "UKCore-Observation-Lab-WhiteCellCount-Example",
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
    resource,
    richard_smith,
    leeds_teaching_hospital,
    white_cell_count,
    red_cell_count,
    pharmacist_jimmy_chuck,
    blood_specimen,
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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Procedure-ExaminationOfSkin-Example",
    ],
)
def test_procedure(resource, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ProcedureSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-RelatedPerson-JoySmith-Example",
    ],
)
def test_related_person(resource, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = RelatedPersonSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-DiagnosticReport-DiagnosticStudiesReport-Example",
        "UKCore-DiagnosticReport-Lab-DiagnosticStudiesReport-Example",
    ],
)
def test_diagnostic_report(
    resource,
    finger_joint_inflamed,
    richard_smith,
    full_blood_count,
    leeds_teaching_hospital,
    blood_specimen,
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = DiagnosticReportSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Condition-BleedingFromEar-Example",
    ],
)
def test_condition(resource, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ConditionSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Device-SoftwareAsAMedicalDevice-Example",
        "UKCore-Device-Sphygmomanometer-Example",
    ],
)
def test_device(resource, leeds_teaching_hospital, cardiology_sjuh):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = DeviceSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Consent-ForInformationAccess-Example",
    ],
)
def test_consent(
    resource, richard_smith, doctor_paul_rastall, white_rose_medical_centre
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ConsentSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Encounter-InpatientEncounter-Example",
    ],
)
def test_encounter(
    resource,
    richard_smith,
    leeds_teaching_hospital,
    consultant_sandra_gose,
    cardiology_sjuh,
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = EncounterSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-EpisodeOfCare-SmokingCessationTherapy-Example",
    ],
)
def test_episode_of_care(resource, richard_smith, leeds_teaching_hospital):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = EpisodeOfCareSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-MessageHeader-Discharge-Example",
    ],
)
def test_message_header(resource, inpatient_encounter, leeds_teaching_hospital):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = MessageHeaderSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-ServiceRequest-Lab-CReactiveProtein-Example",
        "UKCore-ServiceRequest-ColonoscopyRequest-Example",
    ],
)
def test_service_request(
    resource,
    richard_smith,
    pharmacist_jimmy_chuck,
    inpatient_encounter,
    doctor_paul_rastall,
    consultant_sandra_gose,
    hospital_sjuh,
    white_cell_count,
    diagnostic_studies_report,
    leeds_teaching_hospital,
    finger_joint_inflamed,
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ServiceRequestSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-ImagingStudy-CTChestScan-Example",
    ],
)
def test_imaging_study(resource, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ImagingStudySerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-AllergyIntolerance-EnteredInError-Example",
        "UKCore-AllergyIntolerance-Amoxicillin-Example",
    ],
)
def test_allergy_intolerance(
    resource, richard_smith, inpatient_encounter, consultant_sandra_gose
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = AllergyIntoleranceSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Appointment-OrthopaedicSurgery-Example",
    ],
)
def test_appointment(
    resource,
    colonoscopy_request,
    bleeding_from_ear,
    consultant_sandra_gose,
    hospital_sjuh,
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = AppointmentSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Composition-Discharge-Example",
    ],
)
def test_composition(
    resource,
    inpatient_encounter,
    richard_smith,
    timolol_vtm,
    consultant_sandra_gose,
    leeds_teaching_hospital,
    diagnostic_studies_report,
    doctor_paul_rastall,
    examination_of_skin,
    amoxicillin,
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = CompositionSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-FamilyMemberHistory-FatherDiabetes-Example",
    ],
)
def test_family_member_history(resource, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = FamilyMemberHistorySerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Flag-FoodAllergy-Example",
    ],
)
def test_flag(resource, inpatient_encounter, richard_smith, doctor_paul_rastall):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = FlagSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-HealthcareService-OrthopaedicService-Example",
    ],
)
def test_healthcare_service(resource, leeds_teaching_hospital, hospital_sjuh):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = HealthcareServiceSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Task-Colonoscopy-Example",
    ],
)
def test_task(
    resource,
    doctor_paul_rastall,
    consultant_sandra_gose,
    colonoscopy_request,
    inpatient_encounter,
    richard_smith,
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = TaskSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.xfail
@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-List-EmptyList-Example",
    ],
)
def test_list(resource, richard_smith, inpatient_encounter):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = ListSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-MedicationRequest-EyeDrops-Example",
    ],
)
def test_medication_request(
    resource, consultant_sandra_gose, richard_smith, timoptol_eye_drops
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = MedicationRequestSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-MedicationAdministration-TimoptolEyeDrops-Example",
    ],
)
def test_medication_administration(
    resource, richard_smith, timoptol_eye_drops, eye_drops
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = MedicationAdministrationSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-MedicationDispense-EyeDrops-Example",
    ],
)
def test_medication_dispense(
    resource, richard_smith, timoptol_eye_drops, eye_drops, pharmacist_jimmy_chuck
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = MedicationDispenseSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-MedicationStatement-Amoxicillin-Example",
    ],
)
def test_medication_statement(resource, richard_smith):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = MedicationStatementSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-QuestionnaireResponse-InpatientSurvey-Example",
    ],
)
def test_questionare_response(
    resource, consultant_sandra_gose, inpatient_encounter, richard_smith
):
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    serializer = QuestionnaireResponseSerializer(data=copy.deepcopy(payload))
    is_valid = serializer.is_valid()
    assert is_valid, serializer.errors
    assert serializer.to_representation(instance=serializer.validated_data) == payload
