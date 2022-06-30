from django.urls import path
from .import views

urlpatterns = [
    path('', views.apiOverview),
    path('flights/', views.flightList),
    path('create-flight/', views.createFlight),
    path('update-flight/<str:pk>', views.updateFlight)
]
