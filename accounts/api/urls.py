from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from django.urls import path
from .views import AuthView,RegisterAPIView,LogoutAPIView

urlpatterns = [ 
    path('login/', AuthView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('jwt/', obtain_jwt_token),
    path('refresh/', refresh_jwt_token),
]

