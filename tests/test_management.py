import pytest

from api.management.commands.load_example_data import get_examples, load_examples
from api.models.common import BaseProfile


def test_get_examples():
    examples = get_examples()
    assert examples


@pytest.mark.django_db
def test_load_examples():
    assert BaseProfile.objects.count() == 0
    load_examples()
    assert BaseProfile.objects.count() == 50
