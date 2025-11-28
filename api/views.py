from rest_framework.decorators import api_view
from rest_framework.response import Response
from .data import LGA_SCORES


@api_view(['GET'])
def get_lga_scores(request):
    """Return all LGA scores."""
    return Response(LGA_SCORES)


@api_view(['POST'])
def calculate_rankings(request):
    """
    Calculate weighted scores and rankings.
    
    Request body:
    {
        "economic_weight": 40,
        "impact_weight": 0,
        "infrastructure_weight": 65
    }
    
    Formula:
    FinalScore = (EconomicScore * EconomicWeight) + 
                 (ImpactScore * ImpactWeight) + 
                 (InfrastructureScore * InfrastructureWeight)
    """
    economic_weight = request.data.get('economic_weight', 40)
    impact_weight = request.data.get('impact_weight', 0)
    infrastructure_weight = request.data.get('infrastructure_weight', 65)
    
    total_weight = economic_weight + impact_weight + infrastructure_weight
    
    results = []
    for lga in LGA_SCORES:
        if total_weight > 0:
            weighted_score = (
                (lga['economic'] * economic_weight) +
                (lga['impact'] * impact_weight) +
                (lga['infrastructure'] * infrastructure_weight)
            ) / total_weight
        else:
            weighted_score = 0
        
        results.append({
            'id': lga['id'],
            'name': lga['name'],
            'economic': lga['economic'],
            'impact': lga['impact'],
            'infrastructure': lga['infrastructure'],
            'weighted_score': round(weighted_score, 2)
        })
    
    # Sort by weighted score descending
    results.sort(key=lambda x: x['weighted_score'], reverse=True)
    
    # Add rank
    for i, item in enumerate(results):
        item['rank'] = i + 1
    
    return Response({
        'rankings': results,
        'weights': {
            'economic': economic_weight,
            'impact': impact_weight,
            'infrastructure': infrastructure_weight
        }
    })

