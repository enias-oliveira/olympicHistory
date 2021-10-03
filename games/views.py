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
        event_serializer = EventSerializer(data=request.data)
        event_serializer.is_valid(raise_exception=True)

        game = self.get_object()

        sport = Sport.objects.get_or_create(
            name=event_serializer.data.get("sport"),
        )[0]

        new_event = game.events.update_or_create(
            name=event_serializer.data.get("competition"), sport=sport
        )[0]

        serialized_event = GameEventSerializer(new_event)

        return Response(serialized_event.data)

    @events.mapping.get
    def list_events(self, request, pk):
        return Response(
            GameEventSerializer(
                self.get_object().events,
                many=True,
            ).data
        )


class EventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.annotate(
        sport=F("competition__sport__name"),
        competition_name=F("competition__name"),
    )
    serializer_class = EventSerializer
