from typing import Dict, Any, List, Optional
import spacy
import logging
from spacy.matcher import Matcher

class TextAnalyzer:
    """
    Text analysis class.
    """
    def __init__(self):
        # Using the original model; you may consider upgrading to a transformer model later.
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
        # Initialize spaCy Matcher with the shared vocabulary.
        self.matcher = Matcher(self.nlp.vocab)
        
        # Patterns d'adresses plus complets
        address_patterns = [
            # Pattern standard: numéro + type de voie + nom
            [
                {"LIKE_NUM": True},
                {"LOWER": {"IN": ["bis", "ter"]}, "OP": "?"},
                {"LOWER": {"IN": ["rue", "avenue", "boulevard", "impasse", "chemin", "place"]}},
                {"LOWER": {"IN": ["du", "de", "des", "de la", "d'", "l'"]}, "OP": "?"},
                {"IS_ALPHA": True, "OP": "+"}
            ],
            # Pattern inversé: type de voie + nom + numéro
            [
                {"LOWER": {"IN": ["rue", "avenue", "boulevard", "impasse", "chemin", "place"]}},
                {"LOWER": {"IN": ["du", "de", "des", "de la", "d'", "l'"]}, "OP": "?"},
                {"IS_ALPHA": True, "OP": "+"},
                {"LOWER": {"IN": ["numéro", "n°", "n"]}, "OP": "?"},
                {"LIKE_NUM": True},
                {"LOWER": {"IN": ["bis", "ter"]}, "OP": "?"}
            ]
        ]
        
        for idx, pattern in enumerate(address_patterns):
            self.matcher.add(f"ADDRESS_{idx}", [pattern])

    def extract_location(self, text: str) -> Optional[List[str]]:
        """
        Extraction améliorée des locations combinant Matcher et NER.
        """
        try:
            doc = self.nlp(text)
            locations = set()  # Utilisation d'un set pour éviter les doublons

            # Extraction via Matcher
            matches = self.matcher(doc)
            for match_id, start, end in matches:
                address = doc[start:end].text
                locations.add(address)

            # Extraction via NER
            for ent in doc.ents:
                if ent.label_ in ["LOC", "GPE"]:
                    locations.add(ent.text)

            # Nettoyage et validation des résultats
            cleaned_locations = []
            for loc in locations:
                # Suppression des espaces multiples et nettoyage basique
                cleaned_loc = " ".join(loc.split())
                if len(cleaned_loc.split()) >= 2:  # Vérifie que la location contient au moins 2 mots
                    cleaned_locations.append(cleaned_loc)

            if cleaned_locations:
                self.logger.debug(f"Locations trouvées: {cleaned_locations}")
                return cleaned_locations

            # Fallback pour les numéros si aucune location n'est trouvée
            numbers = [token.text for token in doc if token.like_num]
            if numbers:
                self.logger.debug(f"Tokens numériques trouvés: {numbers}")
                return numbers

            return []
        except Exception as e:
            self.logger.error(f"Erreur lors de l'extraction des locations: {e}")
            return None

    def extract_category(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract categories from text.
        Args: Text.
        Returns: Dictionary of categories.
        """
        try:
            text_lower = text.lower()
            for category, keywords in self.categories.items():
                if any(keyword in text_lower for keyword in keywords):
                    return category
            return "autres"
        except Exception as e:
            self.logger.error(f"Error extracting categories: {e}")
            return None

