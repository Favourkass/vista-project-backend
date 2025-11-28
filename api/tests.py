from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class LGAScoresAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_lga_scores(self):
        """Test GET /api/lga-scores/ returns all LGA data"""
        url = '/api/lga-scores/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 20)  # Should have 20 LGAs
        
        # Check structure of first item
        first_lga = response.data[0]
        self.assertIn('id', first_lga)
        self.assertIn('name', first_lga)
        self.assertIn('economic', first_lga)
        self.assertIn('impact', first_lga)
        self.assertIn('infrastructure', first_lga)

    def test_calculate_rankings_default_weights(self):
        """Test POST /api/calculate-rankings/ with default weights"""
        url = '/api/calculate-rankings/'
        data = {
            'economic_weight': 40,
            'impact_weight': 0,
            'infrastructure_weight': 65
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rankings', response.data)
        self.assertIn('weights', response.data)
        
        rankings = response.data['rankings']
        self.assertEqual(len(rankings), 20)
        
        # Check that rankings are sorted by weighted_score descending
        scores = [r['weighted_score'] for r in rankings]
        self.assertEqual(scores, sorted(scores, reverse=True))
        
        # Check that ranks are assigned correctly
        for i, ranking in enumerate(rankings):
            self.assertEqual(ranking['rank'], i + 1)

    def test_calculate_rankings_custom_weights(self):
        """Test POST /api/calculate-rankings/ with custom weights"""
        url = '/api/calculate-rankings/'
        data = {
            'economic_weight': 50,
            'impact_weight': 30,
            'infrastructure_weight': 20
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rankings = response.data['rankings']
        
        # Verify weighted scores are calculated
        for ranking in rankings:
            self.assertIn('weighted_score', ranking)
            self.assertIsInstance(ranking['weighted_score'], (int, float))

    def test_calculate_rankings_zero_weights(self):
        """Test POST /api/calculate-rankings/ with all zero weights"""
        url = '/api/calculate-rankings/'
        data = {
            'economic_weight': 0,
            'impact_weight': 0,
            'infrastructure_weight': 0
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rankings = response.data['rankings']
        
        # All scores should be 0 when all weights are 0
        for ranking in rankings:
            self.assertEqual(ranking['weighted_score'], 0)

    def test_calculate_rankings_missing_weights(self):
        """Test POST /api/calculate-rankings/ with missing weights uses defaults"""
        url = '/api/calculate-rankings/'
        data = {}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should use default weights (40, 0, 65)
        self.assertEqual(response.data['weights']['economic'], 40)
        self.assertEqual(response.data['weights']['impact'], 0)
        self.assertEqual(response.data['weights']['infrastructure'], 65)

