from rest_framework.viewsets import ModelViewSet

from .models import Medal
from .serializers import MedalSerializer


class MedalViewSet(ModelViewSet):
    queryset = Medal.objects.all()
    serializer_class = MedalSerializer
