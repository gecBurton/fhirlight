from rest_framework.viewsets import ModelViewSet

from api.models import Patient, Medication, Observation, Specimen, Location
from api.models.organization import Organization
from api.models.practitioner import Practitioner
from api.serializers.location import LocationSerializer
from api.serializers.medication import MedicationSerializer
from api.serializers.observation import ObservationSerializer
from api.serializers.organization import OrganizationSerializer
from api.serializers.patient import PatientSerializer
from api.serializers.practitioner import PractitionerSerializer
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
