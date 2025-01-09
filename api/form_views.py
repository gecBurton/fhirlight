from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django import forms

from api.forms.organization import OrganizationForm
from api.models.organization import (
    OrganizationProfile,
    OrganizationContactPoint,
    OrganizationAddress,
    OrganizationIdentifier,
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


def organization_view(request, pk=None):
    related_models = [
        OrganizationContactPoint,
        OrganizationAddress,
        OrganizationIdentifier,
    ]
    if pk:
        organization = get_object_or_404(OrganizationProfile, id=pk)
        related_instances = {
            f: f.objects.filter(organization=organization).all() for f in related_models
        }
    else:
        organization = None
        related_instances = {f: f.objects.none() for f in related_models}

    organization_form = OrganizationForm(instance=organization)
    related_forms = build_related_forms(related_instances)

    if request.method == "POST":
        if organization_form.is_valid() and all(
            related_form.is_valid() for related_form in related_forms
        ):
            organization = organization_form.save()
            for related_form in related_forms:
                related_form.save(commit=False)

                for instance in related_form.queryset():
                    instance.organization = organization
                    instance.save()
            return redirect("success_url")

    context = {form.model.__name__: form for form in related_forms}
    context["organization_form"] = organization_form
    return render(request, "api/organization.html", context)
