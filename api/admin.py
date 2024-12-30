from django.contrib import admin
from django.contrib.admin import StackedInline

from api.models import (
    Organization,
    OrganizationContactPoint,
    OrganizationAddress,
    OrganizationIdentifier,
)


class OrganizationContactPointInline(StackedInline):
    model = OrganizationContactPoint
    extra = 0


class OrganizationAddressInline(StackedInline):
    model = OrganizationAddress
    extra = 0


class OrganizationIdentifierInline(StackedInline):
    model = OrganizationIdentifier
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [
        OrganizationContactPointInline,
        OrganizationAddressInline,
        OrganizationIdentifierInline,
    ]


admin.site.register(Organization, OrganizationAdmin)
