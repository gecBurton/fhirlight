import pytest

from api.models import (
    UKCorePatient,
    UKCoreOrganization,
    UKCoreObservation,
    UKCorePractitioner,
    UKCoreLocation,
    UKCoreSpecimen,
)
from api.models.datatypes import Concept


@pytest.fixture
def richard_smith():
    patient = UKCorePatient.objects.create(id="UKCore-Patient-RichardSmith-Example")
    yield patient
    patient.delete()


@pytest.fixture
def consultant_sandra_gose():
    practitioner = UKCorePractitioner.objects.create(
        id="UKCore-Practitioner-ConsultantSandraGose-Example"
    )
    yield practitioner
    practitioner.delete()


@pytest.fixture
def doctor_paul_rastall():
    practitioner = UKCorePractitioner.objects.create(
        id="UKCore-Practitioner-DoctorPaulRastall-Example"
    )
    yield practitioner
    practitioner.delete()


@pytest.fixture
def leeds_teaching_hospital():
    organization = UKCoreOrganization.objects.create(
        id="UKCore-Organization-LeedsTeachingHospital-Example"
    )
    yield organization
    organization.delete()


@pytest.fixture
def white_rose_medical_centre():
    organization = UKCoreOrganization.objects.create(
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
def white_cell_count(observation_type):
    observation = UKCoreObservation.objects.create(
        id="UKCore-Observation-Lab-WhiteCellCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def red_cell_count(observation_type):
    observation = UKCoreObservation.objects.create(
        id="UKCore-Observation-Lab-RedCellCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def finger_joint_inflamed(observation_type):
    observation = UKCoreObservation.objects.create(
        id="UKCore-Observation-FingerJointInflamed-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def full_blood_count(observation_type):
    observation = UKCoreObservation.objects.create(
        id="UKCore-Observation-Group-FullBloodCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def general_practice_nurse_clinic():
    location = UKCoreLocation.objects.create(
        id="UKCore-Location-GeneralPracticeNurseClinic-Example"
    )
    yield location
    location.delete()


@pytest.fixture
def blood_specimen():
    location = UKCoreSpecimen.objects.create(id="UKCore-Specimen-BloodSpecimen-Example")
    yield location
    location.delete()
