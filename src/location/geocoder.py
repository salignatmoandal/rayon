from typing import Optional, Tuple
from opencage.geocoder import OpenCageGeocode
from utils.config import OPENCAGE_API_KEY

class Geolocation:
    """Gère la géolocalisation des adresses et lieux."""
    
    def __init__(self):
        self.geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

    def get_coordinates(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Convertit un lieu en coordonnées géographiques.
        
        Args:
            location: Nom du lieu à géolocaliser
            
        Returns:
            Tuple (latitude, longitude) ou None si non trouvé
        """
        try:
            # Optionally restrict search to a bounding box (e.g., Paris)
            params = {
                'language': 'fr',
                'bounds': '2.224122,48.815575,2.469760,48.902156'  # Paris bounds: SW and NE corners
            }
            results = self.geocoder.geocode(location, **params)
            if results:
                # Optionally, inspect components to ensure result is valid
                components = results[0].get('components', {})
                if components.get('city') or components.get('town') or components.get('village'):
                    return (
                        results[0]['geometry']['lat'],
                        results[0]['geometry']['lng']
                    )
            return None
        except Exception as e:
            print(f"Erreur de géolocalisation : {e}")
            return None

