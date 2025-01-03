from rest_framework.viewsets import ModelViewSet

from api.models import (
    UKCorePatient,
    UKCoreMedication,
    UKCoreObservation,
    UKCoreSpecimen,
    UKCoreLocation,
    UKCoreImmunization,
    UKCoreOperationOutcome,
    UKCoreSlot,
    UKCorePractitionerRole,
    UKCoreSchedule,
    UKCoreQuestionnaire,
    UKCoreProcedure,
    UKCoreRelatedPerson,
    UKCoreDiagnosticReport,
)
from api.models.organization import UKCoreOrganization
from api.models.practitioner import UKCorePractitioner
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
    queryset = UKCoreOrganization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "id"


class PractitionerViewSet(ModelViewSet):
    queryset = UKCorePractitioner.objects.all()
    serializer_class = PractitionerSerializer
    lookup_field = "id"


class PatientViewSet(ModelViewSet):
    queryset = UKCorePatient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = "id"


class MedicationViewSet(ModelViewSet):
    queryset = UKCoreMedication.objects.all()
    serializer_class = MedicationSerializer
    lookup_field = "id"


class ObservationViewSet(ModelViewSet):
    queryset = UKCoreObservation.objects.all()
    serializer_class = ObservationSerializer
    lookup_field = "id"


class SpecimenViewSet(ModelViewSet):
    queryset = UKCoreSpecimen.objects.all()
    serializer_class = SpecimenSerializer
    lookup_field = "id"


class LocationViewSet(ModelViewSet):
    queryset = UKCoreLocation.objects.all()
    serializer_class = LocationSerializer
    lookup_field = "id"


class ImmunizationViewSet(ModelViewSet):
    queryset = UKCoreImmunization.objects.all()
    serializer_class = ImmunizationSerializer
    lookup_field = "id"


class OperationOutcomeViewSet(ModelViewSet):
    queryset = UKCoreOperationOutcome.objects.all()
    serializer_class = OperationOutcomeSerializer
    lookup_field = "id"


class SlotViewSet(ModelViewSet):
    queryset = UKCoreSlot.objects.all()
    serializer_class = SlotSerializer
    lookup_field = "id"


class PractitionerRoleViewSet(ModelViewSet):
    queryset = UKCorePractitionerRole.objects.all()
    serializer_class = PractitionerRoleSerializer
    lookup_field = "id"


class ScheduleViewSet(ModelViewSet):
    queryset = UKCoreSchedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = "id"


class QuestionnaireViewSet(ModelViewSet):
    queryset = UKCoreQuestionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = "id"


class ProcedureViewSet(ModelViewSet):
    queryset = UKCoreProcedure.objects.all()
    serializer_class = ProcedureSerializer
    lookup_field = "id"


class RelatedPersonViewSet(ModelViewSet):
    queryset = UKCoreRelatedPerson.objects.all()
    serializer_class = RelatedPersonSerializer
    lookup_field = "id"


class DiagnosticReportViewSet(ModelViewSet):
    queryset = UKCoreDiagnosticReport.objects.all()
    serializer_class = DiagnosticReportSerializer
    lookup_field = "id"
