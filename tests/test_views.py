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
    ConditionProfile,
    ServiceRequestProfile,
    AllergyIntoleranceProfile,
    MedicationProfile,
    ProcedureProfile,
    MedicationRequestProfile,
)

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
        "UKCore-Observation-Lab-RedCellCount-Example",
        "UKCore-Observation-Lab-WhiteCellCount-Example",
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
        "UKCore-Appointment-OrthopaedicSurgery-Example",
        "UKCore-Composition-Discharge-Example",
        "UKCore-FamilyMemberHistory-FatherDiabetes-Example",
        "UKCore-Flag-FoodAllergy-Example",
        "UKCore-HealthcareService-OrthopaedicService-Example",
        "UKCore-Task-Colonoscopy-Example",
        "UKCore-List-EmptyList-Example",
        "UKCore-MedicationRequest-EyeDrops-Example",
        "UKCore-MedicationAdministration-TimoptolEyeDrops-Example",
        "UKCore-MedicationDispense-EyeDrops-Example",
        "UKCore-MedicationStatement-Amoxicillin-Example",
        "UKCore-QuestionnaireResponse-InpatientSurvey-Example",
        "UKCore-Organization-Maximal-Example",
    ],
)
def test_resource(
    client,
    resource,
    report_code,
    observation_type,
    encounter_code,
    example_patient,
    medication_code,
    allergy_code,
):
    resource_type = resource.split("-")[1].lower()
    with open(f"{TEST_DIR}/data/{resource}.json") as f:
        payload = json.load(f)

    for dependant in extract_reference(payload):
        dependant_resource_type = dependant.split("-")[1].lower()
        resource_types = {
            "patient": (PatientProfile, {}),
            "organization": (OrganizationProfile, {}),
            "practitioner": (PractitionerProfile, {}),
            "location": (LocationProfile, {}),
            "observation": (ObservationProfile, {"code": observation_type}),
            "specimen": (SpecimenProfile, {}),
            "encounter": (EncounterProfile, {"klass": encounter_code}),
            "diagnosticreport": (DiagnosticReportProfile, {"code": report_code}),
            "condition": (ConditionProfile, {"subject": example_patient}),
            "servicerequest": (ServiceRequestProfile, {}),
            "allergyintolerance": (
                AllergyIntoleranceProfile,
                {"code": allergy_code, "patient": example_patient},
            ),
            "medication": (MedicationProfile, {"code": medication_code}),
            "procedure": (ProcedureProfile, {"subject": example_patient}),
            "medicationrequest": (
                MedicationRequestProfile,
                {"subject": example_patient},
            ),
        }

        resource_class, kwargs = resource_types[dependant_resource_type]
        resource_class.objects.create(id=dependant, **kwargs)

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
