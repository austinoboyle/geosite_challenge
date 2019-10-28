from django.urls import include, path
from rest_framework import routers
from api import views

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.RequestList.as_view()),
    path('<int:pk>/', views.RequestDetails.as_view())
]
