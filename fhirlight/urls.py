"""
URL configuration for fhirlight project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import (
    OrganizationViewSet,
    PractitionerViewSet,
    PatientViewSet,
    MedicationViewSet,
    ObservationViewSet,
    SpecimenViewSet,
    LocationViewSet,
    ImmunizationViewSet,
    OperationOutcomeViewSet,
    SlotViewSet,
    PractitionerRoleViewSet,
)

router = routers.DefaultRouter()
router.register(r"Organization", OrganizationViewSet, basename="organization")
router.register(r"Practitioner", PractitionerViewSet, basename="practitioner")
router.register(r"Patient", PatientViewSet, basename="patient")
router.register(r"Medication", MedicationViewSet, basename="medication")
router.register(r"Observation", ObservationViewSet, basename="observation")
router.register(r"Specimen", SpecimenViewSet, basename="specimen")
router.register(r"Location", LocationViewSet, basename="location")
router.register(r"Immunization", ImmunizationViewSet, basename="immunization")
router.register(
    r"OperationOutcome", OperationOutcomeViewSet, basename="operationoutcome"
)
router.register(r"Slot", SlotViewSet, basename="slot")
router.register(
    r"PractitionerRole", PractitionerRoleViewSet, basename="practitionerrole"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
