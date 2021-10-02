from rest_framework.routers import SimpleRouter

from .views import GameViewSet, EventViewSet

router = SimpleRouter()
router.register(r"games", GameViewSet)
router.register(r"events", EventViewSet)

urlpatterns = router.urls
