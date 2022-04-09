from dry_rest_permissions.generics import DRYPermissions
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from movies.models import Movie, MovieTicket
from movies.serializers import MovieSerializer, MovieTicketSerializer


class MovieViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug"


class MovieTicketViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):

    queryset = MovieTicket.objects.all()
    serializer_class = MovieTicketSerializer
    permission_classes = (IsAuthenticated, DRYPermissions)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("movie", "user")
            .filter(user=self.request.user)
        )
