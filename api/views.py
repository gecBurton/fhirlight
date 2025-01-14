from rest_framework.viewsets import ModelViewSet

from api.models import (
    PatientProfile,
    MedicationProfile,
    ObservationProfile,
    SpecimenProfile,
    LocationProfile,
    ImmunizationProfile,
    OperationOutcomeProfile,
    SlotProfile,
    PractitionerRoleProfile,
    ScheduleProfile,
    QuestionnaireProfile,
    ProcedureProfile,
    RelatedPersonProfile,
    DiagnosticReportProfile,
    EncounterProfile,
    ConditionProfile,
    DeviceProfile,
    ConsentProfile,
    EpisodeOfCareProfile,
    MessageHeaderProfile,
    ServiceRequestProfile,
    ImagingStudyProfile,
    AppointmentProfile,
    CompositionProfile,
    FamilyMemberHistoryProfile,
    FlagProfile,
    HealthcareServiceProfile,
    TaskProfile,
    ListProfile,
    MedicationRequestProfile,
    MedicationAdministrationProfile,
    MedicationStatementProfile,
    QuestionnaireResponseProfile,
)
from api.models.medication_dispense import MedicationDispenseProfile
from api.serializers.encounter import EncounterSerializer
from api.models.organization import OrganizationProfile
from api.models.practitioner import PractitionerProfile
from api.serializers import (
    DeviceSerializer,
    ConsentSerializer,
    EpisodeOfCareSerializer,
    MessageHeaderSerializer,
    ServiceRequestSerializer,
    ImagingStudySerializer,
    AppointmentSerializer,
    CompositionSerializer,
    FamilyMemberHistorySerializer,
    FlagSerializer,
    TaskSerializer,
    ListSerializer,
    MedicationRequestSerializer,
    MedicationAdministrationSerializer,
    MedicationDispenseSerializer,
    MedicationStatementSerializer,
    QuestionnaireResponseSerializer,
)
from api.serializers.condition import ConditionSerializer
from api.serializers.diagnostic_report import DiagnosticReportSerializer
from api.serializers.healthcare_service import HealthcareServiceSerializer
from api.serializers.immunization import ImmunizationSerializer
from api.serializers.location import LocationSerializer
from api.serializers.medication import MedicationSerializer
from api.serializers.observation import ObservationSerializer
from api.serializers.operation_outcome import OperationOutcomeSerializer
from api.serializers.organization import OrganizationSerializer
from api.serializers.patient import PatientSerializer
from api.serializers.practitioner import PractitionerSerializer
from api.serializers.practitioner_role import PractitionerRoleSerializer
from api.serializers.procedure import ProcedureSerializer
from api.serializers.questionnaire import QuestionnaireSerializer
from api.serializers.related_person import RelatedPersonSerializer
from api.serializers.schedule import ScheduleSerializer
from api.serializers.slot import SlotSerializer
from api.serializers.specimen import SpecimenSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = OrganizationProfile.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "id"


class PractitionerViewSet(ModelViewSet):
    queryset = PractitionerProfile.objects.all()
    serializer_class = PractitionerSerializer
    lookup_field = "id"


class PatientViewSet(ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientSerializer
    lookup_field = "id"


class MedicationViewSet(ModelViewSet):
    queryset = MedicationProfile.objects.all()
    serializer_class = MedicationSerializer
    lookup_field = "id"


class ObservationViewSet(ModelViewSet):
    queryset = ObservationProfile.objects.all()
    serializer_class = ObservationSerializer
    lookup_field = "id"


class SpecimenViewSet(ModelViewSet):
    queryset = SpecimenProfile.objects.all()
    serializer_class = SpecimenSerializer
    lookup_field = "id"


class LocationViewSet(ModelViewSet):
    queryset = LocationProfile.objects.all()
    serializer_class = LocationSerializer
    lookup_field = "id"


class ImmunizationViewSet(ModelViewSet):
    queryset = ImmunizationProfile.objects.all()
    serializer_class = ImmunizationSerializer
    lookup_field = "id"


class OperationOutcomeViewSet(ModelViewSet):
    queryset = OperationOutcomeProfile.objects.all()
    serializer_class = OperationOutcomeSerializer
    lookup_field = "id"


class SlotViewSet(ModelViewSet):
    queryset = SlotProfile.objects.all()
    serializer_class = SlotSerializer
    lookup_field = "id"


class PractitionerRoleViewSet(ModelViewSet):
    queryset = PractitionerRoleProfile.objects.all()
    serializer_class = PractitionerRoleSerializer
    lookup_field = "id"


class ScheduleViewSet(ModelViewSet):
    queryset = ScheduleProfile.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = "id"


class QuestionnaireViewSet(ModelViewSet):
    queryset = QuestionnaireProfile.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = "id"


class QuestionnaireResponseViewSet(ModelViewSet):
    queryset = QuestionnaireResponseProfile.objects.all()
    serializer_class = QuestionnaireResponseSerializer
    lookup_field = "id"


class ProcedureViewSet(ModelViewSet):
    queryset = ProcedureProfile.objects.all()
    serializer_class = ProcedureSerializer
    lookup_field = "id"


class RelatedPersonViewSet(ModelViewSet):
    queryset = RelatedPersonProfile.objects.all()
    serializer_class = RelatedPersonSerializer
    lookup_field = "id"


class DiagnosticReportViewSet(ModelViewSet):
    queryset = DiagnosticReportProfile.objects.all()
    serializer_class = DiagnosticReportSerializer
    lookup_field = "id"


class ConditionViewSet(ModelViewSet):
    queryset = ConditionProfile.objects.all()
    serializer_class = ConditionSerializer
    lookup_field = "id"


class DeviceViewSet(ModelViewSet):
    queryset = DeviceProfile.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = "id"


class ConsentViewSet(ModelViewSet):
    queryset = ConsentProfile.objects.all()
    serializer_class = ConsentSerializer
    lookup_field = "id"


class EncounterViewSet(ModelViewSet):
    queryset = EncounterProfile.objects.all()
    serializer_class = EncounterSerializer
    lookup_field = "id"


class EpisodeOfCareViewSet(ModelViewSet):
    queryset = EpisodeOfCareProfile.objects.all()
    serializer_class = EpisodeOfCareSerializer
    lookup_field = "id"


class MessageHeaderViewSet(ModelViewSet):
    queryset = MessageHeaderProfile.objects.all()
    serializer_class = MessageHeaderSerializer
    lookup_field = "id"


class ServiceRequestViewSet(ModelViewSet):
    queryset = ServiceRequestProfile.objects.all()
    serializer_class = ServiceRequestSerializer
    lookup_field = "id"


class ImagingStudyViewSet(ModelViewSet):
    queryset = ImagingStudyProfile.objects.all()
    serializer_class = ImagingStudySerializer
    lookup_field = "id"


class AppointmentViewSet(ModelViewSet):
    queryset = AppointmentProfile.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = "id"


class CompositionViewSet(ModelViewSet):
    queryset = CompositionProfile.objects.all()
    serializer_class = CompositionSerializer
    lookup_field = "id"


class FamilyMemberHistoryViewSet(ModelViewSet):
    queryset = FamilyMemberHistoryProfile.objects.all()
    serializer_class = FamilyMemberHistorySerializer
    lookup_field = "id"


class FlagViewSet(ModelViewSet):
    queryset = FlagProfile.objects.all()
    serializer_class = FlagSerializer
    lookup_field = "id"


class HealthcareServiceViewSet(ModelViewSet):
    queryset = HealthcareServiceProfile.objects.all()
    serializer_class = HealthcareServiceSerializer
    lookup_field = "id"


class TaskViewSet(ModelViewSet):
    queryset = TaskProfile.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "id"


class ListViewSet(ModelViewSet):
    queryset = ListProfile.objects.all()
    serializer_class = ListSerializer
    lookup_field = "id"


class MedicationRequestViewSet(ModelViewSet):
    queryset = MedicationRequestProfile.objects.all()
    serializer_class = MedicationRequestSerializer
    lookup_field = "id"


class MedicationAdministrationViewSet(ModelViewSet):
    queryset = MedicationAdministrationProfile.objects.all()
    serializer_class = MedicationAdministrationSerializer
    lookup_field = "id"


class MedicationDispenseViewSet(ModelViewSet):
    queryset = MedicationDispenseProfile.objects.all()
    serializer_class = MedicationDispenseSerializer
    lookup_field = "id"


class MedicationStatementViewSet(ModelViewSet):
    queryset = MedicationStatementProfile.objects.all()
    serializer_class = MedicationStatementSerializer
    lookup_field = "id"
