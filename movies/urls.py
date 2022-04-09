from rest_framework.routers import SimpleRouter

from movies.views import MovieTicketViewSet, MovieViewSet

app_name = "movies"

router = SimpleRouter(trailing_slash=False)
router.register(r"movies", MovieViewSet)
router.register(r"tickets", MovieTicketViewSet)

urlpatterns = router.urls
