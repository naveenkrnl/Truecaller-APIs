from django.urls import path
from .views import (
    DataListSearchAPIView,
    UserDetailAPIView,
    PersonalContactsDetailAPIView
    # UserMarkSpamAPIView

)

urlpatterns = [ 
    path('', DataListSearchAPIView.as_view()),
    path('<pk>/', UserDetailAPIView.as_view()),
    path('p/<pk>/', PersonalContactsDetailAPIView.as_view()),

    # path('<pk>/spam', UserMarkSpamAPIView.as_view()),

]



