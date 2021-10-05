from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from .models import Athlete, Country
from .serializers import AthleteSerializer, CountrySerializer


class AthleteViewSet(ModelViewSet):
    queryset = (
        Athlete.objects.select_related("country")
        .prefetch_related(
            "events",
            "medals",
        )
        .all()
    )
    serializer_class = AthleteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_fields = ["name", "noc"]
