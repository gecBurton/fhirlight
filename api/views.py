from rest_framework.viewsets import ModelViewSet

from api.models import Organization
from api.serializers import OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = "id"
