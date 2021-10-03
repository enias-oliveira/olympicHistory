from django.db.models import Count

from rest_framework.viewsets import ModelViewSet

from .models import Athlete, Country
from .serializers import AthleteSerializer, CountrySerializer


class AthleteViewSet(ModelViewSet):
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.annotate(medals=Count("athletes", distinct=True)).all()
    serializer_class = CountrySerializer
