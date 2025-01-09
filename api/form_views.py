from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit
from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django import forms

from api.models import PatientProfile
from api.models.organization import (
    OrganizationProfile,
    OrganizationContactPoint,
    OrganizationAddress,
    OrganizationIdentifier,
)
from api.models.patient import (
    PatientIdentifier,
    PatientName,
    PatientAddress,
    PatientTelecom,
)


def build_related_forms(related_instances: dict) -> list:
    related_forms = []

    for model, queryset in related_instances.items():
        m = model

        class RelatedForm(forms.ModelForm):
            class Meta:
                model = m
                exclude = ("uuid", "organization", "created_at", "updated_at")

        related_form = modelformset_factory(
            model,
            form=RelatedForm,
            extra=0,
            can_delete=True,
        )

        related_forms.append(related_form(queryset=queryset))

    return related_forms


def form_builder(main_model, related_models, success_url, request, pk=None):
    if pk:
        main_instance = get_object_or_404(main_model, id=pk)
        related_instances = {
            f: f.objects.filter(profile=main_instance).all() for f in related_models
        }
    else:
        main_instance = None
        related_instances = {f: f.objects.none() for f in related_models}

    class ProfileForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Submit("submit", "Submit"))

        class Meta:
            model = main_model
            exclude = ("id",)

    profile_form = ProfileForm(instance=main_instance)
    related_forms = build_related_forms(related_instances)

    if request.method == "POST":
        if profile_form.is_valid() and all(
            related_form.is_valid() for related_form in related_forms
        ):
            profile = profile_form.save()
            for related_form in related_forms:
                related_form.save(commit=False)

                for instance in related_form.queryset():
                    instance.profile = profile
                    instance.save()
            return redirect(success_url)

    context = {form.model.__name__: form for form in related_forms}
    context["main_form"] = profile_form
    return context


def organization_view(request, pk=None):
    main_model = OrganizationProfile
    related_models = [
        OrganizationContactPoint,
        OrganizationAddress,
        OrganizationIdentifier,
    ]
    context = form_builder(main_model, related_models, "success_url", request, pk)
    return render(request, "api/organization.html", context)


def patient_view(request, pk=None):
    main_model = PatientProfile
    related_models = [
        PatientIdentifier,
        PatientTelecom,
        PatientName,
        PatientAddress,
    ]
    context = form_builder(main_model, related_models, "success_url", request, pk)
    return render(request, "api/patient.html", context)
