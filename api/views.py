from rest_framework.viewsets import ModelViewSet

from api.models.organization import Organization
from api.models.practitioner import Practitioner
from api.serializers.organization import OrganizationSerializer
from api.serializers.practitioner import PractitionerSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "id"


class PractitionerViewSet(ModelViewSet):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    lookup_field = "id"
