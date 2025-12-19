from django.urls import path

from .views import PlaceList

urlpatterns = [
    path('', PlaceList.as_view()),
]