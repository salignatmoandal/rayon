from typing import Optional
import logging
from speech.recognizer import SpeechRecognizer
from text.analyzer import TextAnalyzer
from location.geocoder import Geolocation
from location.suggestions import AISuggester
from utils.logger import setup_logger
from display.map_display import MapDisplay

class voiceNavigationApp:
    def __init__(self):
        self.logger = setup_logger()
        self.speech_recognizer = SpeechRecognizer()
        self.text_analyzer = TextAnalyzer()
        self.geolocation = Geolocation()
        self.ai_suggester = AISuggester()
        self.map_display = MapDisplay()

    def process_voice_command(self) -> bool:
        """
        Process voice command and handle the entire workflow.
        Returns:
            bool: True if processing successful, False otherwise
        """
        try:
            print("\n📝 Instructions:")
            print("1. Wait for the '🎤 Start speaking now...' prompt")
            print("2. Speak clearly into the microphone")
            print("3. Pause briefly when finished speaking\n")
            
            # 1. Voice recognition
            result = self.speech_recognizer.listen_and_convert()
            if not result:
                print("❌ Voice recognition failed. Tips:")
                print("- Speak louder and more clearly")
                print("- Reduce background noise")
                print("- Move closer to the microphone\n")
                return False
            
            text = result["text"]
            print(f"✅ Recognized text: {text}")

            # 2. Analyze the intent

            locations = self.text_analyzer.extract_location(text)
            if not locations:
                self.logger.error("No location found in the command")
                return False
            category = self.text_analyzer.extract_category(text)
            location = locations[0] if locations else None
            if not category:
                self.logger.info("No category found in the command")
                return False
            
            # 3. Geolocation
            coordinates = self.geolocation.get_coordinates(location)
            if not coordinates:
                self.logger.error("Error getting coordinates")
                return False

            # 4. AI suggestion
            suggestions = self.ai_suggester.get_suggestions(
                location=location,
                coordinates=coordinates,
                category=category
            )
            if not suggestions:
                self.logger.error("No suggestions found")
                return False
            
            print(f"📍 Location: {location}")
            print(f"🎯 Coordinates: {coordinates}")
            print(f"📝 Found {len(suggestions)} suggestions")
            
            # 5. Display the map
            self.map_display.display_map(coordinates, suggestions)
            return True
        
        except Exception as e:
            self.logger.error(f"Error processing voice command: {e}")
            return False
     
def main():
    app = voiceNavigationApp()
    print("Welcome to the voice navigation app!")
    
    while True:
        try:
            input("Press Enter to start talking (or Ctrl+C to quit)...")
            if app.process_voice_command():
                print("Processing successful! The map has been updated.")
            else:
                print("The processing failed, please try again.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
