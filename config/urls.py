from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Lagos LGA API',
        'endpoints': {
            'lga-scores': '/api/lga-scores/',
            'calculate-rankings': '/api/calculate-rankings/'
        }
    })

urlpatterns = [
    path('api', api_root, name='api-root'),
    path('api/', include('api.urls')),
]

