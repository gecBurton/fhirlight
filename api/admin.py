from django.contrib import admin
from django.contrib.admin import StackedInline
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from api.models.common import BaseProfile
from api.models.organization import (
    OrganizationProfile,
    OrganizationTelecom,
    OrganizationAddress,
    OrganizationIdentifier,
)


class UKCoreAdmin(PolymorphicParentModelAdmin):
    child_models = (OrganizationProfile,)


class OrganizationContactPointInline(StackedInline):
    model = OrganizationTelecom
    extra = 0


class OrganizationAddressInline(StackedInline):
    model = OrganizationAddress
    extra = 0


class OrganizationIdentifierInline(StackedInline):
    model = OrganizationIdentifier
    extra = 0


class OrganizationAdmin(PolymorphicChildModelAdmin):
    base_model = BaseProfile

    inlines = [
        OrganizationContactPointInline,
        OrganizationAddressInline,
        OrganizationIdentifierInline,
    ]


admin.site.register(BaseProfile, UKCoreAdmin)
admin.site.register(OrganizationProfile, OrganizationAdmin)
