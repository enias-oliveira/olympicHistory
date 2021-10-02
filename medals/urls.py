from rest_framework.routers import SimpleRouter

from .views import MedalViewSet

router = SimpleRouter()
router.register(r"medals", MedalViewSet)

urlpatterns = router.urls
