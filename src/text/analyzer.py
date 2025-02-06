from typing import Dict, Any, List, Optional
import spacy
import logging
class TextAnalyzer:
    """
    Text analysis class.
    """
    def __init__(self):
        self.nlp = spacy.load("fr_core_news_sm")
        self.categories = {
            "restaurant": ["restaurant", "café", "bar", "brasserie"],
            "commerce": ["magasin", "boutique", "supermarket"],
            "transport": ["gare", "train", "bus", "métro"],
            "tourisme": ["musée", "monument", "site", "piscine"],
            "autres": ["autre", "rien", "rien de pertinent"],
            "culture": ["cinéma", "théâtre", "bibliothèque", "musée", "monument", "site", "piscine"]
        }
        self.logger = logging.getLogger(__name__)

    def extract_location(self, text: str) -> Optional[List[str]]:
        """
        Extract locations from text.
        Args: Text.
        Returns: List of locations.
        """
        try:
            doc = self.nlp(text)
            locations = [ent.text for ent in doc.ents if ent.label_ ]
            return locations
        except Exception as e:
            self.logger.error(f"Error extracting locations: {e}")
            return None
    
    def extract_categories(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract categories from text.
        Args: Text.
        Returns: Dictionary of categories.
        """
        try:
           text = text.lower()
           for category, keywords in self.categories.items():
               if any(keyword in text for keyword in keywords):
                   return category
           return "autres"
        except Exception as e:
            self.logger.error(f"Error extracting categories: {e}")
            return None
            
            