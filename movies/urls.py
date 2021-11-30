from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieList.as_view(), name='index'),
    path('soon/', views.MovieList.as_view(),name='soon'),
]