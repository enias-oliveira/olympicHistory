from rest_framework.routers import SimpleRouter

from .views import GameViewSet

router = SimpleRouter()
router.register(r"games", GameViewSet)

urlpatterns = router.urls
