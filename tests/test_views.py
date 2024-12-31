import json
import os.path

import pytest
from django.urls import reverse


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
    ],
)
def test_resource(client, resource):
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
