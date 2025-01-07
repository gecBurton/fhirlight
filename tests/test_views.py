import json
import os.path

import pytest
from django.urls import reverse

from api.management.commands.load_example_data import extract_reference
from api.models import (
    PatientProfile,
    OrganizationProfile,
    PractitionerProfile,
    LocationProfile,
    ObservationProfile,
    SpecimenProfile,
    EncounterProfile,
    DiagnosticReportProfile,
)
from api.models.datatypes import Concept

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-Organization-LeedsTeachingHospital-Example",
        "UKCore-Organization-WhiteRoseMedicalCentre-Example",
        "UKCore-Practitioner-ConsultantSandraGose-Example",
        "UKCore-Practitioner-DoctorPaulRastall-Example",
        "UKCore-Practitioner-PharmacistJimmyChuck-Example",
        "UKCore-Patient-BabyPatient-Example",
        "UKCore-Patient-RichardSmith-Example",
        "UKCore-Medication-COVID-Vaccine-Example",
        "UKCore-Medication-TimololVTM-Example",
        "UKCore-Medication-TimoptolEyeDrops-Example",
        "UKCore-Observation-24HourBloodPressure-Example",
        "UKCore-Observation-AwarenessOfDiagnosis-Example",
        "UKCore-Observation-BreathingNormally-Example",
        "UKCore-Observation-DrugUse-Example",
        "UKCore-Observation-VitalSigns-BloodPressure-Example",
        "UKCore-Observation-VitalSigns-BMI-Example",
        "UKCore-Observation-VitalSigns-BodyHeight-Example",
        "UKCore-Observation-VitalSigns-BodyTemperature-Example",
        "UKCore-Observation-VitalSigns-BodyWeight-Example",
        "UKCore-Observation-VitalSigns-HeadCircumference-Example",
        "UKCore-Observation-VitalSigns-HeartRate-Example",
        "UKCore-Observation-VitalSigns-OxygenSaturation-Example",
        "UKCore-Observation-VitalSigns-RespiratoryRate-Example",
        "UKCore-Specimen-UrineSpecimen-Example",
        "UKCore-Specimen-BloodSpecimen-Example",
        "UKCore-Location-GeneralPracticeNurseClinic-Example",
        "UKCore-Location-CardiologySJUH-Example",
        "UKCore-Location-HospitalSJUH-Example",
        "UKCore-Immunization-InfluenzaVaccine-Example",
        "UKCore-OperationOutcome-DateError-Example",
        "UKCore-Slot-AvailableWalkInVisit-Example",
        "UKCore-PractitionerRole-GeneralPractitioner-Example",
        "UKCore-Schedule-Immunization-Example",
        "UKCore-Questionnaire-InpatientSurvey-Example",
        "UKCore-Procedure-ExaminationOfSkin-Example",
        "UKCore-RelatedPerson-JoySmith-Example",
        "UKCore-DiagnosticReport-DiagnosticStudiesReport-Example",
        "UKCore-DiagnosticReport-Lab-DiagnosticStudiesReport-Example",
        "UKCore-Encounter-InpatientEncounter-Example",
        "UKCore-Condition-BleedingFromEar-Example",
        "UKCore-Consent-ForInformationAccess-Example",
        "UKCore-EpisodeOfCare-SmokingCessationTherapy-Example",
        "UKCore-MessageHeader-Discharge-Example",
        "UKCore-ServiceRequest-Lab-CReactiveProtein-Example",
        "UKCore-ServiceRequest-ColonoscopyRequest-Example",
        "UKCore-ImagingStudy-CTChestScan-Example",
    ],
)
def test_resource(
    client,
    resource,
):
    resource_type = resource.split("-")[1].lower()
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    for dependant in extract_reference(payload):
        dependant_resource_type = dependant.split("-")[1].lower()
        resource_types = {
            "patient": PatientProfile,
            "organization": OrganizationProfile,
            "practitioner": PractitionerProfile,
            "location": LocationProfile,
            "observation": ObservationProfile,
            "specimen": SpecimenProfile,
            "encounter": EncounterProfile,
            "diagnosticreport": DiagnosticReportProfile,
        }
        if dependant_resource_type == "observation":
            code = Concept.objects.filter(
                valueset=Concept.VALUESET.UK_CORE_OBSERVATION_TYPE
            ).first()
            resource_types[dependant_resource_type].objects.create(
                id=dependant, code=code
            )
        elif dependant_resource_type == "encounter":
            code = Concept.objects.filter(
                valueset=Concept.VALUESET.V3_ACT_ENCOUNTER_CODE
            ).first()
            resource_types[dependant_resource_type].objects.create(
                id=dependant, klass=code
            )
        elif dependant_resource_type == "diagnosticreport":
            code = Concept.objects.filter(
                valueset=Concept.VALUESET.UK_CORE_REPORT_CODE
            ).first()
            resource_types[dependant_resource_type].objects.create(
                id=dependant, code=code
            )
        else:
            resource_types[dependant_resource_type].objects.create(id=dependant)

    url_list = reverse(f"{resource_type}-list")

    post_response = client.post(
        url_list, json.dumps(payload), content_type="application/json"
    )
    assert post_response.status_code == 201, post_response.json()
    assert post_response.json() == payload

    url_detail = reverse(f"{resource_type}-detail", kwargs={"id": payload["id"]})
    get_response = client.get(url_detail)
    assert get_response.status_code == 200
    assert get_response.json() == payload

    get_response = client.get(url_list)
    assert get_response.status_code == 200
    assert payload in [entry["resource"] for entry in get_response.json()["entry"]]
