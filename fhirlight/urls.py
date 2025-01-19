from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import (
    AllergyIntoleranceViewSet,
    AppointmentViewSet,
    CompositionViewSet,
    ConditionViewSet,
    ConsentViewSet,
    DeviceViewSet,
    DiagnosticReportViewSet,
    EncounterViewSet,
    EpisodeOfCareViewSet,
    FamilyMemberHistoryViewSet,
    FlagViewSet,
    HealthcareServiceViewSet,
    ImagingStudyViewSet,
    ImmunizationViewSet,
    ListViewSet,
    LocationViewSet,
    MedicationAdministrationViewSet,
    MedicationDispenseViewSet,
    MedicationRequestViewSet,
    MedicationStatementViewSet,
    MedicationViewSet,
    MessageHeaderViewSet,
    ObservationViewSet,
    OperationOutcomeViewSet,
    OrganizationViewSet,
    PatientViewSet,
    PractitionerRoleViewSet,
    PractitionerViewSet,
    ProcedureViewSet,
    QuestionnaireResponseViewSet,
    QuestionnaireViewSet,
    RelatedPersonViewSet,
    ScheduleViewSet,
    ServiceRequestViewSet,
    SlotViewSet,
    SpecimenViewSet,
    TaskViewSet,
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
    r"OperationOutcome",
    OperationOutcomeViewSet,
    basename="operationoutcome",
)
router.register(r"Slot", SlotViewSet, basename="slot")
router.register(
    r"PractitionerRole",
    PractitionerRoleViewSet,
    basename="practitionerrole",
)
router.register(r"ScheduleRole", ScheduleViewSet, basename="schedule")
router.register(r"Questionnaire", QuestionnaireViewSet, basename="questionnaire")
router.register(
    r"QuestionnaireResponse",
    QuestionnaireResponseViewSet,
    basename="questionnaireresponse",
)
router.register(r"Procedure", ProcedureViewSet, basename="procedure")
router.register(r"RelatedPerson", RelatedPersonViewSet, basename="relatedperson")
router.register(
    r"DiagnosticReport",
    DiagnosticReportViewSet,
    basename="diagnosticreport",
)
router.register(r"Condition", ConditionViewSet, basename="condition")
router.register(r"Device", DeviceViewSet, basename="device")
router.register(r"Consent", ConsentViewSet, basename="consent")
router.register(r"Encounter", EncounterViewSet, basename="encounter")
router.register(r"EpisodeOfCare", EpisodeOfCareViewSet, basename="episodeofcare")
router.register(r"MessageHeader", MessageHeaderViewSet, basename="messageheader")
router.register(r"ServiceRequest", ServiceRequestViewSet, basename="servicerequest")
router.register(r"ImagingStudy", ImagingStudyViewSet, basename="imagingstudy")
router.register(r"Appointment", AppointmentViewSet, basename="appointment")
router.register(r"Composition", CompositionViewSet, basename="composition")
router.register(
    r"FamilyMemberHistory",
    FamilyMemberHistoryViewSet,
    basename="familymemberhistory",
)
router.register(r"Flag", FlagViewSet, basename="flag")
router.register(
    r"HealthCareService",
    HealthcareServiceViewSet,
    basename="healthcareservice",
)
router.register(r"Task", TaskViewSet, basename="task")
router.register(r"List", ListViewSet, basename="list")
router.register(
    r"MedicationRequest",
    MedicationRequestViewSet,
    basename="medicationrequest",
)
router.register(
    r"MedicationAdministration",
    MedicationAdministrationViewSet,
    basename="medicationadministration",
)
router.register(
    r"MedicationDispense",
    MedicationDispenseViewSet,
    basename="medicationdispense",
)
router.register(
    r"MedicationStatement",
    MedicationStatementViewSet,
    basename="medicationstatement",
)
router.register(
    r"AllergyIntolerance",
    AllergyIntoleranceViewSet,
    basename="allergyintolerance",
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
]
