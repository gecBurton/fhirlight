import json
import os.path

import pytest
from django.urls import reverse


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.django_db
@pytest.mark.parametrize(
    "organization",
    [
        "UKCore-Organization-LeedsTeachingHospital-Example",
        "UKCore-Organization-WhiteRoseMedicalCentre-Example",
    ],
)
def test_organizations(client, organization):
    with open(f"{TEST_DIR}/data/{organization}.json") as f:
        payload = json.load(f)

    url = reverse("organization-list")

    post_response = client.post(
        url, json.dumps(payload), content_type="application/json"
    )
    assert post_response.status_code == 201, post_response.json()
    assert post_response.json() == payload

    url = reverse("organization-detail", kwargs={"id": payload["id"]})
    get_response = client.get(url)
    assert get_response.status_code == 200
    assert get_response.json() == payload
