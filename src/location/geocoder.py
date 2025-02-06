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
            results = self.geocoder.geocode(location, language='fr')
            if results:
                return (
                    results[0]['geometry']['lat'],
                    results[0]['geometry']['lng']
                )
            return None
        except Exception as e:
            print(f"Erreur de géolocalisation : {e}")
            return None