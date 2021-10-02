from django.db.models import F

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Game, Sport, Event
from .serializers import GameSerializer, GameEventSerializer, EventSerializer


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True, methods=["post"])
    def events(self, request, pk):
        event_serializer = GameEventSerializer(data=request.data)

        game = self.get_object()
        event_serializer.is_valid(raise_exception=True)

        sport = Sport.objects.get_or_create(
            name=event_serializer.data.get("sport"),
        )[0]

        new_event = game.events.create(
            name=event_serializer.data.get("competition"), sport=sport
        )

        serialized_event = GameEventSerializer(new_event)

        return Response(serialized_event.data)

    @events.mapping.get
    def list_events(self, request, pk):
        return Response(
            EventSerializer(
                self.get_object().events,
                many=True,
            ).data
        )


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.annotate(sport=F("competition__sport__name"))
    serializer_class = EventSerializer
