import json
import os.path

import pytest
from django.urls import reverse

from api.models import Patient, Organization

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "resource, patient, organization",
    [
        ("UKCore-Organization-LeedsTeachingHospital-Example", None, None),
        ("UKCore-Organization-WhiteRoseMedicalCentre-Example", None, None),
        ("UKCore-Practitioner-ConsultantSandraGose-Example", None, None),
        ("UKCore-Practitioner-DoctorPaulRastall-Example", None, None),
        ("UKCore-Practitioner-PharmacistJimmyChuck-Example", None, None),
        ("UKCore-Patient-BabyPatient-Example", None, None),
        ("UKCore-Patient-RichardSmith-Example", None, None),
        ("UKCore-Medication-COVID-Vaccine-Example", None, None),
        ("UKCore-Medication-TimololVTM-Example", None, None),
        ("UKCore-Medication-TimoptolEyeDrops-Example", None, None),
        (
            "UKCore-Observation-24HourBloodPressure-Example",
            "UKCore-Patient-RichardSmith-Example",
            "UKCore-Organization-LeedsTeachingHospital-Example",
        ),
        (
            "UKCore-Observation-AwarenessOfDiagnosis-Example",
            "UKCore-Patient-RichardSmith-Example",
            None,
        ),
        (
            "UKCore-Observation-BreathingNormally-Example",
            "UKCore-Patient-RichardSmith-Example",
            "UKCore-Organization-LeedsTeachingHospital-Example",
        ),
        (
            "UKCore-Observation-DrugUse-Example",
            "UKCore-Patient-RichardSmith-Example",
            "UKCore-Organization-LeedsTeachingHospital-Example",
        ),
    ],
)
def test_resource(client, resource, patient, organization):
    if patient:
        Patient.objects.create(id=patient)
    if organization:
        Organization.objects.create(id=organization)

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
