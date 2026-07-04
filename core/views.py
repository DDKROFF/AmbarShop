from rest_framework import viewsets
from .models import SiteInfo
from .serializers import SiteInfoSerializer


class SiteInfoViewSet(viewsets.ModelViewSet):
    queryset = SiteInfo.objects.all()
    serializer_class = SiteInfoSerializer
    lookup_field = 'key'
