import json
import os.path

import pytest
from django.urls import reverse

from api.management.commands.load_example_data import extract_reference
from api.models import (
    AllergyIntoleranceProfile,
    ConditionProfile,
    DiagnosticReportProfile,
    EncounterProfile,
    HealthcareServiceProfile,
    LocationProfile,
    MedicationProfile,
    MedicationRequestProfile,
    ObservationProfile,
    OrganizationProfile,
    PatientProfile,
    PractitionerProfile,
    ProcedureProfile,
    RelatedPersonProfile,
    ServiceRequestProfile,
    SpecimenProfile,
)
from tests.utils import prepare_payload

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource",
    [
        "UKCore-AllergyIntolerance-Amoxicillin-Example",
        "UKCore-AllergyIntolerance-EnteredInError-Example",
        "UKCore-AllergyIntolerance-Maximal-Example",
        "UKCore-Appointment-Maximal-Example",
        "UKCore-Appointment-OrthopaedicSurgery-Example",
        "UKCore-Composition-Discharge-Example",
        "UKCore-Condition-BleedingFromEar-Example",
        "UKCore-Condition-Maximal-Example",
        "UKCore-Consent-ForInformationAccess-Example",
        "UKCore-DiagnosticReport-DiagnosticStudiesReport-Example",
        "UKCore-DiagnosticReport-Lab-DiagnosticStudiesReport-Example",
        "UKCore-Encounter-InpatientEncounter-Example",
        "UKCore-EpisodeOfCare-SmokingCessationTherapy-Example",
        "UKCore-FamilyMemberHistory-FatherDiabetes-Example",
        "UKCore-Flag-FoodAllergy-Example",
        "UKCore-HealthcareService-OrthopaedicService-Example",
        "UKCore-ImagingStudy-CTChestScan-Example",
        "UKCore-Immunization-InfluenzaVaccine-Example",
        "UKCore-List-EmptyList-Example",
        "UKCore-Location-CardiologySJUH-Example",
        "UKCore-Location-GeneralPracticeNurseClinic-Example",
        "UKCore-Location-HospitalSJUH-Example",
        "UKCore-Medication-COVID-Vaccine-Example",
        "UKCore-Medication-TimololVTM-Example",
        "UKCore-Medication-TimoptolEyeDrops-Example",
        "UKCore-MedicationAdministration-TimoptolEyeDrops-Example",
        "UKCore-MedicationDispense-EyeDrops-Example",
        "UKCore-MedicationRequest-EyeDrops-Example",
        "UKCore-MedicationStatement-Amoxicillin-Example",
        "UKCore-MessageHeader-Discharge-Example",
        "UKCore-Observation-24HourBloodPressure-Example",
        "UKCore-Observation-AwarenessOfDiagnosis-Example",
        "UKCore-Observation-BreathingNormally-Example",
        "UKCore-Observation-DrugUse-Example",
        "UKCore-Observation-Lab-RedCellCount-Example",
        "UKCore-Observation-Lab-WhiteCellCount-Example",
        "UKCore-Observation-VitalSigns-BMI-Example",
        "UKCore-Observation-VitalSigns-BloodPressure-Example",
        "UKCore-Observation-VitalSigns-BodyHeight-Example",
        "UKCore-Observation-VitalSigns-BodyTemperature-Example",
        "UKCore-Observation-VitalSigns-BodyWeight-Example",
        "UKCore-Observation-VitalSigns-HeadCircumference-Example",
        "UKCore-Observation-VitalSigns-HeartRate-Example",
        "UKCore-Observation-VitalSigns-OxygenSaturation-Example",
        "UKCore-Observation-VitalSigns-RespiratoryRate-Example",
        "UKCore-OperationOutcome-DateError-Example",
        "UKCore-Organization-LeedsTeachingHospital-Example",
        "UKCore-Organization-Maximal-Example",
        "UKCore-Organization-WhiteRoseMedicalCentre-Example",
        "UKCore-Patient-BabyPatient-Example",
        "UKCore-Patient-RichardSmith-Example",
        "UKCore-Practitioner-ConsultantSandraGose-Example",
        "UKCore-Practitioner-DoctorPaulRastall-Example",
        "UKCore-Practitioner-Maximal-Example",
        "UKCore-Practitioner-PharmacistJimmyChuck-Example",
        "UKCore-PractitionerRole-GeneralPractitioner-Example",
        "UKCore-PractitionerRole-Maximal-Example",
        "UKCore-Procedure-ExaminationOfSkin-Example",
        "UKCore-Questionnaire-InpatientSurvey-Example",
        "UKCore-QuestionnaireResponse-InpatientSurvey-Example",
        "UKCore-RelatedPerson-JoySmith-Example",
        "UKCore-RelatedPerson-Maximal-Example",
        "UKCore-Schedule-Immunization-Example",
        "UKCore-ServiceRequest-ColonoscopyRequest-Example",
        "UKCore-ServiceRequest-Lab-CReactiveProtein-Example",
        "UKCore-Slot-AvailableWalkInVisit-Example",
        "UKCore-Specimen-BloodSpecimen-Example",
        "UKCore-Specimen-UrineSpecimen-Example",
        "UKCore-Task-Colonoscopy-Example",
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
            "healthcareservice": (HealthcareServiceProfile, {}),
            "relatedperson": (RelatedPersonProfile, {"patient": example_patient}),
        }

        resource_class, kwargs = resource_types[dependant_resource_type]
        resource_class.objects.create(id=dependant, **kwargs)

    url_list = reverse(f"{resource_type}-list")

    post_response = client.post(
        url_list, json.dumps(payload), content_type="application/json"
    )
    assert post_response.status_code == 201, post_response.json()
    assert post_response.json() == prepare_payload(payload)

    url_detail = reverse(f"{resource_type}-detail", kwargs={"id": payload["id"]})
    get_response = client.get(url_detail)
    assert get_response.status_code == 200
    assert get_response.json() == prepare_payload(payload)

    get_response = client.get(url_list)
    assert get_response.status_code == 200
    assert prepare_payload(payload) in [
        entry["resource"] for entry in get_response.json()["entry"]
    ]

    delete_response = client.delete(url_detail)
    assert delete_response.status_code == 204
    assert not delete_response.content

    get_response = client.get(url_detail)
    assert get_response.status_code == 404

    profile_name = payload["resourceType"] + "Profile"
    assert get_response.json() == {
        "detail": f"No {profile_name} matches the given query."
    }
