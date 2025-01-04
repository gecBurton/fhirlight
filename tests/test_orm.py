import pytest

from api.models.common import UKCore


@pytest.mark.django_db
def test_orm(pharmacist_jimmy_chuck):
    obj = UKCore.objects.filter(
        polymorphic_ctype__model__in=["ukcoreorganization", "ukcorepractitioner"]
    ).first()
    assert obj == pharmacist_jimmy_chuck
