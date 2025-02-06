import speech_recognition as sr
from typing import Optional, Dict, Any
import logging
from utils.config import AUDIO_SAMPLE_RATE

class AudioRecorder:
    """
    Record audio from the microphone and convert to text.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(sample_rate=AUDIO_SAMPLE_RATE)
        self.logger = logging.getLogger(__name__)
        
        # Configuration
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.non_speaking_duration = 0.5
        
    def calibrate(self, duration: int = 5) -> bool:
        """
        Calibrate the microphone.
        Args: Duration of the calibration in seconds.
        Returns: True if the calibration is successful, False otherwise.
        """
        try:
            self.logger.info(f"Calibrating for {duration} seconds...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
            self.logger.info("Calibration complete.")
            return True
        except Exception as e:
            self.logger.error(f"Error during calibration: {e}")
            return False
            
    def record(self, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Record audio from the microphone.
        Args: Timeout in seconds.
        Returns: Audio data as a dictionary.
        """
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout)
                
            return {
                "audio_data": audio,
                "sample_rate": audio.sample_rate,
                "duration": len(audio.get_raw_data()) / (audio.sample_rate * 2),
                "channels": 1
            }
        except Exception as e:
            self.logger.error(f"Error recording audio: {e}")
            return None
            
    def record_with_vad(self, MIN_DURATION: float= 0.5, MAX_DURATION: float= 10.0) -> Optional[Dict[str, Any]]:
        """
        Record audio from the microphone with voice activity detection.
        """
        try:
            self.logger.info("Starting voice activity detection...")
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    phrase_time_limit=MAX_DURATION,
                    timeout=MIN_DURATION
                )
                duration = len(audio.get_raw_data()) / (audio.sample_rate * 2)
                return {
                    "audio_data": audio,
                    "sample_rate": audio.sample_rate,
                    "duration": duration,
                    "channels": 1,
                    "vad": True
                }
        except sr.WaitTimeoutError:
            self.logger.warning("Time out recording audio")
            return None
        except sr.RequestError as e:
            self.logger.error(f"API unavailable or unresponsive: {e}")
            return None
                