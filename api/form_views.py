from django.shortcuts import redirect, render, get_object_or_404

from api.forms.organization import (
    OrganizationForm,
    OrganizationContactPointFormSet,
    OrganizationAddressFormSet,
    OrganizationIdentifierFormSet,
)
from api.models.organization import (
    OrganizationProfile,
    OrganizationContactPoint,
    OrganizationAddress,
    OrganizationIdentifier,
)


def organization_view(request, pk=None):
    if pk:
        organization = get_object_or_404(OrganizationProfile, id=pk)
        contact_points = organization.organizationcontactpoint_set.all()
        addresses = organization.organizationaddress_set.all()
        identifiers = organization.organizationidentifier_set.all()
    else:
        organization = None
        contact_points = OrganizationContactPoint.objects.none()
        addresses = OrganizationAddress.objects.none()
        identifiers = OrganizationIdentifier.objects.none()

    organization_form = OrganizationForm(instance=organization)
    contact_point_formset = OrganizationContactPointFormSet(queryset=contact_points)
    address_formset = OrganizationAddressFormSet(queryset=addresses)
    identifier_formset = OrganizationIdentifierFormSet(
        request.POST, queryset=identifiers
    )

    if request.method == "POST":
        if organization_form.is_valid() and contact_point_formset.is_valid():
            organization = organization_form.save()
            contact_points = contact_point_formset.save(commit=False)
            for contact_point in contact_points:
                contact_point.organization = organization
                contact_point.save()
            return redirect("success_url")

    context = {
        "organization_form": organization_form,
        "contact_point_formset": contact_point_formset,
        "address_formset": address_formset,
        "identifier_formset": identifier_formset,
    }
    return render(request, "api/organization.html", context)
