from rest_framework.routers import SimpleRouter

from .views import AthleteViewSet

router = SimpleRouter()
router.register(r"athletes", AthleteViewSet)

urlpatterns = router.urls
