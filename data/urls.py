from django.urls import path, include
from .views import home_view
urlpatterns = [
    path('', home_view),
    path('api/data/', include("data.api.urls")),

]
