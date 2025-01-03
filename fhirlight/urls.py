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
    ScheduleViewSet,
    QuestionnaireViewSet,
    ProcedureViewSet,
    RelatedPersonViewSet,
    DiagnosticReportViewSet,
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
router.register(r"ScheduleRole", ScheduleViewSet, basename="schedule")
router.register(r"Questionnaire", QuestionnaireViewSet, basename="questionnaire")
router.register(r"Procedure", ProcedureViewSet, basename="procedure")
router.register(r"RelatedPerson", RelatedPersonViewSet, basename="relatedperson")
router.register(
    r"DiagnosticReport", DiagnosticReportViewSet, basename="diagnosticreport"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
