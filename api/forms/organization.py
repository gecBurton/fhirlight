from django import forms

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit

from api.models import OrganizationProfile


class OrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit"))

    class Meta:
        model = OrganizationProfile
        fields = ("name",)
