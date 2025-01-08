from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit

from api.models import (
    OrganizationProfile,
    OrganizationContactPoint,
    OrganizationAddress,
    OrganizationIdentifier,
)
from django.forms import modelformset_factory


class OrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = OrganizationProfile
        fields = ("name",)


class OrganizationContactPointForm(forms.ModelForm):
    class Meta:
        model = OrganizationContactPoint
        fields = ("system", "value", "use", "rank", "period_start", "period_end")


class OrganizationAddressForm(forms.ModelForm):
    class Meta:
        model = OrganizationAddress
        exclude = ("uuid", "organization", "created_at", "updated_at")


class OrganizationIdentifierForm(forms.ModelForm):
    class Meta:
        model = OrganizationIdentifier
        exclude = ("uuid", "organization", "created_at", "updated_at")


OrganizationContactPointFormSet = modelformset_factory(
    OrganizationContactPoint,
    form=OrganizationContactPointForm,
    extra=0,
    can_delete=True,
)

OrganizationAddressFormSet = modelformset_factory(
    OrganizationAddress, form=OrganizationAddressForm, extra=0, can_delete=True
)

OrganizationIdentifierFormSet = modelformset_factory(
    OrganizationIdentifier, form=OrganizationIdentifierForm, extra=0, can_delete=True
)
