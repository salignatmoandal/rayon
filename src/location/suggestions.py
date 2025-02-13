import re
import json
from typing import List, Dict, Tuple, Optional
from openai import OpenAI
from utils.config import OPENAI_API_KEY

class AISuggester:
    """Gère les suggestions de lieux via l'IA."""
    
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def extract_json(self, text: str) -> Optional[str]:
        """
        Extrait un objet JSON depuis une chaîne qui pourrait contenir du texte additionnel.
        """
        match = re.search(r'(\[.*\])', text, re.DOTALL)
        if match:
            return match.group(1)
        return None

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
            location: Lieu de référence (ex : "12 rue du Louvre")
            category: Catégorie souhaitée
            coordinates: Coordonnées du lieu
            radius_km: Rayon de recherche en km
            
        Returns:
            Liste des suggestions. Si aucune suggestion n'est trouvée,
            renvoie au moins un objet avec les coordonnées.
        """
        prompt = (
            f"En tant qu'assistant touristique expert, "
            f"en vous basant sur l'adresse '{location}', qui correspond à une rue spécifique, "
            f"suggérez 3 lieux à visiter dans un rayon de {radius_km} km "
            f"dans la catégorie '{category}'. "
            "Veuillez répondre uniquement avec un tableau JSON conforme au format ci-dessous, "
            "sans aucun texte additionnel :\n\n"
            "[\n"
            "    {\"nom\": \"Nom du lieu\", \"description\": \"Description\", \"categorie\": \"Catégorie\"}\n"
            "]"
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Vous êtes un guide touristique expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            json_str = self.extract_json(content)
            if not json_str:
                raise ValueError("La réponse ne contient pas un JSON valide.")
            
            suggestions = json.loads(json_str)
            
            # Si la liste est vide, nous préparons un fallback
            if not suggestions:
                suggestions = [{
                    "nom": "Aucune suggestion trouvée",
                    "description": "Aucune suggestion disponible pour le moment.",
                    "categorie": category
                }]
            
            # Ajout des coordonnées aux suggestions
            for suggestion in suggestions:
                suggestion["coordinates"] = coordinates
                
            return suggestions
            
        except Exception as e:
            print(f"Erreur lors de la génération des suggestions : {e}")
            # En cas d'erreur, renvoyer un fallback contenant au moins les coordonnées
            return [{
                "nom": "Aucune suggestion trouvée",
                "description": "Aucune suggestion disponible pour le moment.",
                "categorie": category,
                "coordinates": coordinates
            }]

