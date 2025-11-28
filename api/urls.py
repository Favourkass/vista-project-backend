from django.urls import path
from . import views

urlpatterns = [
    path('lga-scores/', views.get_lga_scores, name='lga-scores'),
    path('calculate-rankings/', views.calculate_rankings, name='calculate-rankings'),
]

