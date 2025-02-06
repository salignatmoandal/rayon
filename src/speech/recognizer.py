from typing import Optional, Dict, Any
import speech_recognition as sr
from audio.processor import AudioProcessor

class SpeechRecognizer:
    """
    Speech recognition class.
    """
    
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.recognizer = sr.Recognizer()

    def convert_to_text(self,audio_data:sr.AudioData) -> Optional[str]:
        """
        Convert audio data to text.
        Args: Audio data.
        Returns: string of text.
        """
        try:
            return self.recognizer.recognize_google(
                audio_data, 
                language="fr-FR"
            )
        except sr.UnknownValueError:
            self.logger.warning("Unable to recognize speech")
            return None
        except sr.RequestError as e:
            self.logger.error(f"API unavailable or unresponsive: {e}")
            return None
    def listen_and_convert(self) -> Optional[Dict[str, Any]]:
        """
        Record audio, clean it and convert to text.
        """
        try:
            # Record audio
            audio = self.audio_processor.record_audio()
            if not audio:
                return None
            
            # Clean audio
            cleaned_audio = self.audio_processor.reduce_noise(audio)
            if cleaned_audio is None:
                return None
            
            # Convert to text
            text = self.convert_to_text(cleaned_audio)
            if not text:
                return None
            
            return {
                "text": text,
                "audio_duration": len(audio.get_raw_data()) / (audio.sample_rate * 2),
                "channels": 1
            }
        except Exception as e:
            self.logger.error(f"Error recognizing speech: {e}")
            return None
                
                
            