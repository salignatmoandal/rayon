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
        # Define a basic pattern for addresses: a number followed by a street indicator and at least one token.
        address_pattern = [
            {"LIKE_NUM": True},
            {"LOWER": {"IN": ["rue", "avenue", "boulevard", "impasse", "chemin", "place"]}},
            {"IS_ALPHA": True, "OP": "+"}
        ]
        self.matcher.add("ADDRESS", [address_pattern])

    def extract_location(self, text: str) -> Optional[List[str]]:
        """
        Enhanced extraction of locations using spaCy's NER and Matcher.
        Returns a list of identified locations/entities, aiming to capture address coordinates accurately.
        """
        try:
            doc = self.nlp(text)
            # Debug: log token-level information.
            tokens_info = [(token.text, token.pos_, token.dep_) for token in doc]
            self.logger.debug(f"Token-level info: {tokens_info}")

            # First, use the Matcher to find address-like patterns.
            matches = self.matcher(doc)
            addresses = [doc[start:end].text for match_id, start, end in matches]
            if addresses:
                self.logger.debug(f"Addresses found by matcher: {addresses}")
                return addresses

            # If no address-like pattern is found, fall back to NER.
            ner_locations = [ent.text for ent in doc.ents if ent.label_]
            if ner_locations:
                self.logger.debug(f"Locations found by NER: {ner_locations}")
                return ner_locations

            # Further fallback: return numeric tokens (e.g., potential street numbers) if available.
            numbers = [token.text for token in doc if token.like_num]
            if numbers:
                self.logger.debug(f"Fallback numeric tokens: {numbers}")
                return numbers

            return []
        except Exception as e:
            self.logger.error(f"Error extracting locations: {e}")
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

