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
    PractitionerRole,
    ScheduleProfile,
    QuestionnaireProfile,
    ProcedureProfile,
    RelatedPersonProfile,
    DiagnosticReportProfile,
)
from api.models.organization import OrganizationProfile
from api.models.practitioner import PractitionerProfile
from api.serializers.diagnostic_report import DiagnosticReportSerializer
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
    queryset = PractitionerRole.objects.all()
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
