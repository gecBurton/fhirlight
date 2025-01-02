import pytest

from api.models import Patient, Organization, Observation, Practitioner, Location
from api.models.datatypes import Concept


@pytest.fixture
def richard_smith():
    patient = Patient.objects.create(id="UKCore-Patient-RichardSmith-Example")
    yield patient
    patient.delete()


@pytest.fixture
def consultant_sandra_gose():
    practitioner = Practitioner.objects.create(
        id="UKCore-Practitioner-ConsultantSandraGose-Example"
    )
    yield practitioner
    practitioner.delete()


@pytest.fixture
def doctor_paul_rastall():
    practitioner = Practitioner.objects.create(
        id="UKCore-Practitioner-DoctorPaulRastall-Example"
    )
    yield practitioner
    practitioner.delete()


@pytest.fixture
def leeds_teaching_hospital():
    Oorganization = Organization.objects.create(
        id="UKCore-Organization-LeedsTeachingHospital-Example"
    )
    yield Oorganization
    Oorganization.delete()


@pytest.fixture
def white_rose_medical_centre():
    Oorganization = Organization.objects.create(
        id="UKCore-Organization-WhiteRoseMedicalCentre-Example"
    )
    yield Oorganization
    Oorganization.delete()


@pytest.fixture
def observation_type():
    return Concept.objects.filter(
        valueset=Concept.VALUESET.UK_CORE_OBSERVATION_TYPE
    ).first()


@pytest.fixture
def white_cell_count(observation_type):
    observation = Observation.objects.create(
        id="UKCore-Observation-Lab-WhiteCellCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def red_cell_count(observation_type):
    observation = Observation.objects.create(
        id="UKCore-Observation-Lab-RedCellCount-Example", code=observation_type
    )
    yield observation
    observation.delete()


@pytest.fixture
def general_practice_nurse_clinic(observation_type):
    location = Location.objects.create(
        id="UKCore-Location-GeneralPracticeNurseClinic-Example"
    )
    yield location
    location.delete()


#
