
import pytest

from api.models import (
    PatientProfile,
    OrganizationProfile,
    ObservationProfile,
    PractitionerProfile,
    LocationProfile,
    SpecimenProfile,
    EncounterProfile,
    DiagnosticReportProfile,
    ConditionProfile,
    ServiceRequestProfile,
    ProcedureProfile,
    AllergyIntoleranceProfile,
    MedicationProfile,
)
from api.models.datatypes import Concept


@pytest.fixture
def richard_smith():
    patient = PatientProfile.objects.create(id="UKCore-Patient-RichardSmith-Example")
    yield patient
    patient.delete()


@pytest.fixture
def example_patient():
    patient = PatientProfile.objects.create(id="example-patient")
    yield patient
    patient.delete()


@pytest.fixture
def consultant_sandra_gose():
    practitioner = PractitionerProfile.objects.create(
        id="UKCore-Practitioner-ConsultantSandraGose-Example"
    )
    yield practitioner
    practitioner.delete()


@pytest.fixture
def doctor_paul_rastall():
    practitioner = PractitionerProfile.objects.create(
        id="UKCore-Practitioner-DoctorPaulRastall-Example"
    )
    yield practitioner
    practitioner.delete()


@pytest.fixture
def pharmacist_jimmy_chuck():
    practitioner = PractitionerProfile.objects.create(
        id="UKCore-Practitioner-PharmacistJimmyChuck-Example"
    )
    yield practitioner
    practitioner.delete()


@pytest.fixture
def leeds_teaching_hospital():
    organization = OrganizationProfile.objects.create(
        id="UKCore-Organization-LeedsTeachingHospital-Example"
    )
    yield organization
    organization.delete()


@pytest.fixture
def white_rose_medical_centre():
    organization = OrganizationProfile.objects.create(
        id="UKCore-Organization-WhiteRoseMedicalCentre-Example"
    )
    yield organization
    organization.delete()


@pytest.fixture
def observation_type():
    return Concept.objects.filter(
        valueset=Concept.VALUESET.UK_CORE_OBSERVATION_TYPE
    ).first()


@pytest.fixture
def encounter_code():
    return Concept.objects.filter(
        valueset=Concept.VALUESET.V3_ACT_ENCOUNTER_CODE
    ).first()


@pytest.fixture
def allergy_code():
    return Concept.objects.filter(
        valueset=Concept.VALUESET.UK_CORE_ALLERGY_CODE
    ).first()


@pytest.fixture
def medication_code():
    return Concept.objects.filter(
        valueset=Concept.VALUESET.UK_CORE_MEDICATION_CODE
    ).first()


@pytest.fixture
def report_code():
    return Concept.objects.filter(valueset=Concept.VALUESET.UK_CORE_REPORT_CODE).first()


@pytest.fixture
def white_cell_count(observation_type):
    observation = ObservationProfile.objects.create(
        id="UKCore-Observation-Lab-WhiteCellCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def red_cell_count(observation_type):
    observation = ObservationProfile.objects.create(
        id="UKCore-Observation-Lab-RedCellCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def finger_joint_inflamed(observation_type):
    observation = ObservationProfile.objects.create(
        id="UKCore-Observation-FingerJointInflamed-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def full_blood_count(observation_type):
    observation = ObservationProfile.objects.create(
        id="UKCore-Observation-Group-FullBloodCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def general_practice_nurse_clinic():
    location = LocationProfile.objects.create(
        id="UKCore-Location-GeneralPracticeNurseClinic-Example"
    )
    yield location
    location.delete()


@pytest.fixture
def cardiology_sjuh():
    location = LocationProfile.objects.create(
        id="UKCore-Location-CardiologySJUH-Example"
    )
    yield location
    location.delete()


@pytest.fixture
def hospital_sjuh():
    location = LocationProfile.objects.create(id="UKCore-Location-HospitalSJUH-Example")
    yield location
    location.delete()


@pytest.fixture
def blood_specimen():
    specimen = SpecimenProfile.objects.create(
        id="UKCore-Specimen-BloodSpecimen-Example"
    )
    yield specimen
    specimen.delete()


@pytest.fixture
def inpatient_encounter(encounter_code):
    encounter = EncounterProfile.objects.create(
        id="UKCore-Encounter-InpatientEncounter-Example", klass=encounter_code
    )
    yield encounter
    encounter.delete()


@pytest.fixture
def diagnostic_studies_report(report_code):
    encounter = DiagnosticReportProfile.objects.create(
        id="UKCore-DiagnosticReport-DiagnosticStudiesReport-Example", code=report_code
    )
    yield encounter
    encounter.delete()


@pytest.fixture
def bleeding_from_ear(richard_smith):
    condition = ConditionProfile.objects.create(
        id="UKCore-Condition-BleedingFromEar-Example", subject=richard_smith
    )
    yield condition
    condition.delete()


@pytest.fixture
def colonoscopy_request():
    service_request = ServiceRequestProfile.objects.create(
        id="UKCore-ServiceRequest-ColonoscopyRequest-Example"
    )
    yield service_request
    service_request.delete()


@pytest.fixture
def examination_of_skin(richard_smith):
    procedure = ProcedureProfile.objects.create(
        id="UKCore-Procedure-ExaminationOfSkin-Example", subject=richard_smith
    )
    yield procedure
    procedure.delete()


@pytest.fixture
def amoxicillin(allergy_code, richard_smith):
    allergy_intolerance = AllergyIntoleranceProfile.objects.create(
        id="UKCore-AllergyIntolerance-Amoxicillin-Example",
        code=allergy_code,
        patient=richard_smith,
    )
    yield allergy_intolerance
    allergy_intolerance.delete()


@pytest.fixture
def timolol_vtm(medication_code):
    medication = MedicationProfile.objects.create(
        id="UKCore-Medication-TimololVTM-Example", code=medication_code
    )
    yield medication
    medication.delete()
