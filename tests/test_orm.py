import pytest

from api.models.common import BaseProfile


@pytest.mark.django_db
def test_orm(pharmacist_jimmy_chuck):
    obj = BaseProfile.objects.filter(
        polymorphic_ctype__model__in=["organizationprofile", "practitionerprofile"]
    ).first()
    assert obj == pharmacist_jimmy_chuck
