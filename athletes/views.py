from rest_framework.viewsets import ModelViewSet

from .models import Athlete
from .serializers import AthleteSerializer


class AthleteViewSet(ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer
