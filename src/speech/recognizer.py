from typing import Optional, Dict, Any
import speech_recognition as sr
import logging
from audio.recorder import AudioRecorder
from audio.processor import AudioProcessor

class SpeechRecognizer:
    """
    Speech recognition class.
    """
    
    def __init__(self):
        self.audio_recorder = AudioRecorder()
        self.audio_processor = AudioProcessor()
        self.recognizer = sr.Recognizer()
        self.logger = logging.getLogger(__name__)

    def convert_to_text(self, audio_data: sr.AudioData) -> Optional[str]:
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
            # Calibration et enregistrement
            if not self.audio_recorder.calibrate():
                return None
                
            recording = self.audio_recorder.record()
            if not recording:
                return None
                
            # Nettoyage audio
            cleaned_audio = self.audio_processor.reduce_noise(recording["audio_data"])
            if not cleaned_audio:
                return None
                
            # Conversion en texte
            text = self.convert_to_text(cleaned_audio)
            if not text:
                return None
                
            return {
                "text": text,
                "audio_duration": recording["duration"],
                "channels": recording["channels"]
            }
        except Exception as e:
            self.logger.error(f"Error recognizing speech: {e}")
            return None
                
                
            