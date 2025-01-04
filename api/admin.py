from django.contrib import admin
from django.contrib.admin import StackedInline
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from api.models.common import UKCore
from api.models.organization import (
    UKCoreOrganization,
    OrganizationContactPoint,
    OrganizationAddress,
    OrganizationIdentifier,
)


class UKCoreAdmin(PolymorphicParentModelAdmin):
    child_models = (UKCoreOrganization,)


class OrganizationContactPointInline(StackedInline):
    model = OrganizationContactPoint
    extra = 0


class OrganizationAddressInline(StackedInline):
    model = OrganizationAddress
    extra = 0


class OrganizationIdentifierInline(StackedInline):
    model = OrganizationIdentifier
    extra = 0


class OrganizationAdmin(PolymorphicChildModelAdmin):
    base_model = UKCore

    inlines = [
        OrganizationContactPointInline,
        OrganizationAddressInline,
        OrganizationIdentifierInline,
    ]


admin.site.register(UKCore, UKCoreAdmin)
admin.site.register(UKCoreOrganization, OrganizationAdmin)
