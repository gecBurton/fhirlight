from rest_framework.viewsets import ModelViewSet

from api.models import (
    Patient,
    Medication,
    Observation,
    Specimen,
    Location,
    Immunization,
    OperationOutcome,
    Slot,
    PractitionerRole,
    Schedule,
    Questionnaire,
)
from api.models.organization import Organization
from api.models.practitioner import Practitioner
from api.serializers.immunization import ImmunizationSerializer
from api.serializers.location import LocationSerializer
from api.serializers.medication import MedicationSerializer
from api.serializers.observation import ObservationSerializer
from api.serializers.operation_outcome import OperationOutcomeSerializer
from api.serializers.organization import OrganizationSerializer
from api.serializers.patient import PatientSerializer
from api.serializers.practitioner import PractitionerSerializer
from api.serializers.practitioner_role import PractitionerRoleSerializer
from api.serializers.questionnaire import QuestionnaireSerializer
from api.serializers.schedule import ScheduleSerializer
from api.serializers.slot import SlotSerializer
from api.serializers.specimen import SpecimenSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "id"


class PractitionerViewSet(ModelViewSet):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    lookup_field = "id"


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = "id"


class MedicationViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    lookup_field = "id"


class ObservationViewSet(ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    lookup_field = "id"


class SpecimenViewSet(ModelViewSet):
    queryset = Specimen.objects.all()
    serializer_class = SpecimenSerializer
    lookup_field = "id"


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = "id"


class ImmunizationViewSet(ModelViewSet):
    queryset = Immunization.objects.all()
    serializer_class = ImmunizationSerializer
    lookup_field = "id"


class OperationOutcomeViewSet(ModelViewSet):
    queryset = OperationOutcome.objects.all()
    serializer_class = OperationOutcomeSerializer
    lookup_field = "id"


class SlotViewSet(ModelViewSet):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    lookup_field = "id"


class PractitionerRoleViewSet(ModelViewSet):
    queryset = PractitionerRole.objects.all()
    serializer_class = PractitionerRoleSerializer
    lookup_field = "id"


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    lookup_field = "id"


class QuestionnaireViewSet(ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = "id"
