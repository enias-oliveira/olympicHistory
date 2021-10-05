from rest_framework.viewsets import ModelViewSet

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


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
