from typing import List, Dict, Tuple, Optional
import json
from openai import OpenAI
from utils.config import OPENAI_API_KEY

class AISuggester:
    """Gère les suggestions de lieux via l'IA."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def get_suggestions(
        self, 
        location: str,
        category: str,
        coordinates: Tuple[float, float],
        radius_km: int = 5
    ) -> List[Dict]:
        """
        Obtient des suggestions de lieux à proximité.
        
        Args:
            location: Lieu de référence
            category: Catégorie souhaitée
            coordinates: Coordonnées du lieu
            radius_km: Rayon de recherche en km
            
        Returns:
            Liste des suggestions
        """
        prompt = f"""En tant qu'assistant touristique, suggérez 3 lieux à visiter près de {location} 
        (dans un rayon de {radius_km}km) dans la catégorie {category}.
        
        Format JSON attendu:
        [
            {{"nom": "Nom du lieu", "description": "Description", "categorie": "Catégorie"}}
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Vous êtes un guide touristique expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            suggestions = json.loads(response.choices[0].message.content)
            
            # Ajout des coordonnées aux suggestions
            for suggestion in suggestions:
                suggestion["coordinates"] = coordinates
                
            return suggestions
            
        except Exception as e:
            print(f"Erreur lors de la génération des suggestions : {e}")
            return []