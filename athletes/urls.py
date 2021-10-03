from rest_framework.routers import SimpleRouter

from .views import AthleteViewSet, CountryViewSet

router = SimpleRouter()
router.register(r"athletes", AthleteViewSet)
router.register(r"countries", CountryViewSet)

urlpatterns = router.urls
