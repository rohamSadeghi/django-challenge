from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="HAMI BOURSE APIs")

urlpatterns = [
    path('v1/accounts/', include("accounts.api.urls")),


    path('v1/docs/', schema_view),
]
