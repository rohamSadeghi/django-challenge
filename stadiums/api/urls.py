from django.urls import path, include
from rest_framework import routers

from stadiums.api.views import MatchViewSet

router = routers.SimpleRouter()
router.register(r'matches', MatchViewSet, basename='matches')

urlpatterns = [
    path('', include(router.urls)),
]
