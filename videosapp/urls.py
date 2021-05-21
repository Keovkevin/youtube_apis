from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.SearchView, name= 'search'),
    path('videos/', views.StoredVideoView, name = 'videos'),

]