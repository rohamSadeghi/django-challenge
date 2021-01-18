from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from stadiums.api.serializers import MatchSerializer
from stadiums.models import Match


class MatchViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    """

        list:
            Return all matches , ordered by most recently added.

        retrieve:
            Return a specific match detail.
        purchase_seat:
            Purchase seat based on specific match.


    """
    serializer_class = MatchSerializer
    queryset = Match.objects.filter(
        is_enable=True,
        execute_time_range__startswith__gt=timezone.now()
    ).select_related('stadium').order_by('-id')
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, )


    @action(detail=True, methods=['post'], url_path='purchase-seat')
    def purchase_seat(self, request, *args, **kwargs):
        match = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(match=match, user=request.user)
        return Response(serializer.data)
