from rest_framework.routers import SimpleRouter

from movies.views import MovieViewSet

app_name = "movies"

router = SimpleRouter(trailing_slash=False)
router.register(r"movies", MovieViewSet)

urlpatterns = router.urls
