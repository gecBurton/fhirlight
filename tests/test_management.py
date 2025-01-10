import pytest
from django.core.management import call_command

from api.models.common import BaseProfile


@pytest.mark.django_db
def test_load_example_data():
    assert BaseProfile.objects.count() == 0
    call_command("load_example_data")
    assert BaseProfile.objects.count() == 63
