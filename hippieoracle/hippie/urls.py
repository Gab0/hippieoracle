from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/map', views.showMap, name='showMap')
]
