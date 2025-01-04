import json
import os.path

import pytest
from django.urls import reverse

from api.models import (
    PatientProfile,
    OrganizationProfile,
    PractitionerProfile,
    LocationProfile,
    ObservationProfile,
    SpecimenProfile,
)
from api.models.datatypes import Concept

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource, dependants",
    [
        ("UKCore-Organization-LeedsTeachingHospital-Example", []),
        ("UKCore-Organization-WhiteRoseMedicalCentre-Example", []),
        ("UKCore-Practitioner-ConsultantSandraGose-Example", []),
        ("UKCore-Practitioner-DoctorPaulRastall-Example", []),
        ("UKCore-Practitioner-PharmacistJimmyChuck-Example", []),
        ("UKCore-Patient-BabyPatient-Example", []),
        ("UKCore-Patient-RichardSmith-Example", []),
        ("UKCore-Medication-COVID-Vaccine-Example", []),
        ("UKCore-Medication-TimololVTM-Example", []),
        ("UKCore-Medication-TimoptolEyeDrops-Example", []),
        (
            "UKCore-Observation-24HourBloodPressure-Example",
            [
                "UKCore-Patient-RichardSmith-Example",
                "UKCore-Organization-LeedsTeachingHospital-Example",
            ],
        ),
        (
            "UKCore-Observation-AwarenessOfDiagnosis-Example",
            ["UKCore-Patient-RichardSmith-Example"],
        ),
        (
            "UKCore-Observation-BreathingNormally-Example",
            [
                "UKCore-Patient-RichardSmith-Example",
                "UKCore-Organization-LeedsTeachingHospital-Example",
            ],
        ),
        (
            "UKCore-Observation-DrugUse-Example",
            [
                "UKCore-Patient-RichardSmith-Example",
                "UKCore-Organization-LeedsTeachingHospital-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-BloodPressure-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-BMI-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-BodyHeight-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-BodyTemperature-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-BodyWeight-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-HeadCircumference-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-HeartRate-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-OxygenSaturation-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Observation-VitalSigns-RespiratoryRate-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Specimen-UrineSpecimen-Example",
            [
                "UKCore-Practitioner-ConsultantSandraGose-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Specimen-BloodSpecimen-Example",
            [
                "UKCore-Practitioner-ConsultantSandraGose-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Location-GeneralPracticeNurseClinic-Example",
            ["UKCore-Organization-WhiteRoseMedicalCentre-Example"],
        ),
        (
            "UKCore-Location-CardiologySJUH-Example",
            ["UKCore-Organization-LeedsTeachingHospital-Example"],
        ),
        (
            "UKCore-Location-HospitalSJUH-Example",
            ["UKCore-Organization-LeedsTeachingHospital-Example"],
        ),
        (
            "UKCore-Immunization-InfluenzaVaccine-Example",
            [
                "UKCore-Location-GeneralPracticeNurseClinic-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        ("UKCore-OperationOutcome-DateError-Example", []),
        ("UKCore-Slot-AvailableWalkInVisit-Example", []),
        (
            "UKCore-PractitionerRole-GeneralPractitioner-Example",
            [
                "UKCore-Practitioner-DoctorPaulRastall-Example",
                "UKCore-Organization-WhiteRoseMedicalCentre-Example",
            ],
        ),
        (
            "UKCore-Schedule-Immunization-Example",
            ["UKCore-Location-GeneralPracticeNurseClinic-Example"],
        ),
        ("UKCore-Questionnaire-InpatientSurvey-Example", []),
        (
            "UKCore-Procedure-ExaminationOfSkin-Example",
            ["UKCore-Patient-RichardSmith-Example"],
        ),
        (
            "UKCore-RelatedPerson-JoySmith-Example",
            ["UKCore-Patient-RichardSmith-Example"],
        ),
        (
            "UKCore-DiagnosticReport-DiagnosticStudiesReport-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Observation-FingerJointInflamed-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-DiagnosticReport-Lab-DiagnosticStudiesReport-Example",
            [
                "UKCore-Organization-LeedsTeachingHospital-Example",
                "UKCore-Observation-Group-FullBloodCount-Example",
                "UKCore-Specimen-BloodSpecimen-Example",
                "UKCore-Patient-RichardSmith-Example",
            ],
        ),
        (
            "UKCore-Condition-BleedingFromEar-Example",
            ["UKCore-Patient-RichardSmith-Example"],
        ),
    ],
)
def test_resource(client, resource, dependants):
    for dependant in dependants:
        dependant_resource_type = dependant.split("-")[1].lower()
        resource_types = {
            "patient": PatientProfile,
            "organization": OrganizationProfile,
            "practitioner": PractitionerProfile,
            "location": LocationProfile,
            "observation": ObservationProfile,
            "specimen": SpecimenProfile,
        }
        code = Concept.objects.filter(
            valueset=Concept.VALUESET.UK_CORE_OBSERVATION_TYPE
        ).first()
        if dependant_resource_type == "observation":
            resource_types[dependant_resource_type].objects.create(
                id=dependant, code=code
            )
        else:
            resource_types[dependant_resource_type].objects.create(id=dependant)

    resource_type = resource.split("-")[1].lower()
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    url = reverse(f"{resource_type}-list")

    post_response = client.post(
        url, json.dumps(payload), content_type="application/json"
    )
    assert post_response.status_code == 201, post_response.json()
    assert post_response.json() == payload

    url = reverse(f"{resource_type}-detail", kwargs={"id": payload["id"]})
    get_response = client.get(url)
    assert get_response.status_code == 200
    assert get_response.json() == payload
