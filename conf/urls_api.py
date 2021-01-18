from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="TICKET ONLINE APIs")

urlpatterns = [
    path('v1/accounts/', include("accounts.api.urls")),
    path('v1/stadiums/', include("stadiums.api.urls")),


    path('v1/docs/', schema_view),
]
