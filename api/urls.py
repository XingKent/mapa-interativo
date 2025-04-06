from django.urls import path
from . import views

urlpatterns = [
    path('indicadores/<str:uf>/', views.indicadores_estado, name='indicadores_estado'),
]
