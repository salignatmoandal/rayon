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
        
        # Ajustement des paramètres de reconnaissance
        self.recognizer.energy_threshold = 3000  # Réduire la sensibilité
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5

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
            # 1. Calibration avec feedback
            self.logger.info("Starting calibration...")
            if not self.audio_recorder.calibrate():
                self.logger.error("Calibration failed")
                return None
                
            # 2. Enregistrement avec feedback visuel
            self.logger.info("Listening...")
            recording = self.audio_recorder.record_with_vad(
                MIN_DURATION=1.0,
                MAX_DURATION=15.0
            )
            
            if not recording:
                self.logger.error("No audio recorded")
                return None
                
            # 3. Réduction du bruit avec feedback
            self.logger.info("Processing audio...")
            cleaned_audio = self.audio_processor.reduce_noise(recording["audio_data"])
            if not cleaned_audio:
                self.logger.error("Audio cleaning failed")
                return None
                
            # 4. Multiple tentatives de reconnaissance
            for attempt in range(2):
                try:
                    text = self.recognizer.recognize_google(
                        cleaned_audio,
                        language="fr-FR",
                        show_all=False
                    )
                    if text:
                        return {
                            "text": text,
                            "audio_duration": recording["duration"],
                            "channels": recording["channels"],
                            "confidence": "high" if attempt == 0 else "medium"
                        }
                except sr.UnknownValueError:
                    self.logger.warning(f"Attempt {attempt + 1} failed")
                    continue
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Error in speech recognition: {e}")
            return None
                
                
            