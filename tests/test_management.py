import pytest

from api.management.commands.load_example_data import load_examples
from api.models.common import BaseProfile


@pytest.mark.django_db
def test_load_examples():
    assert BaseProfile.objects.count() == 0
    load_examples()
    assert BaseProfile.objects.count() == 62
