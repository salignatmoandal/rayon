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
        
        # Adjust recognition parameters for better detection
        self.recognizer.energy_threshold = 1000  # Lower for better sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 2.0  # Increase for more patience
        self.recognizer.phrase_threshold = 0.5
        self.non_speaking_duration = 1.0
        
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
            print("🎤 Recording...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout)
            print("✅ Recording finished")
            self.logger.debug(f"Level of sound detected: {self.recognizer.energy_threshold}")
            
            return {
                "audio_data": audio,
                "sample_rate": audio.sample_rate,
                "duration": len(audio.get_raw_data()) / (audio.sample_rate * 2),
                "channels": 1
            }
        except Exception as e:
            self.logger.error(f"Error recording audio: {e}")
            return None
            
    def record_with_vad(self, MIN_DURATION: float = 1.0, MAX_DURATION: float = 20.0) -> Optional[Dict[str, Any]]:
        """
        Record audio with Voice Activity Detection (VAD).
        Args:
            MIN_DURATION: Minimum duration of recording in seconds
            MAX_DURATION: Maximum duration of recording in seconds
        Returns:
            Dictionary containing audio data and metadata, or None if failed
        """
        try:
            self.logger.info("Starting voice activity detection...")
            print("🎤 Start speaking now...")
            
            with self.microphone as source:
                # Adjust for ambient noise before each recording
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=MAX_DURATION,
                        phrase_time_limit=MAX_DURATION
                    )
                    print("✅ Recording completed")
                    
                    duration = len(audio.get_raw_data()) / (audio.sample_rate * 2)
                    if duration < MIN_DURATION:
                        self.logger.warning(f"Recording too short: {duration:.2f}s")
                        return None
                        
                    return {
                        "audio_data": audio,
                        "sample_rate": audio.sample_rate,
                        "duration": duration,
                        "channels": 1,
                        "vad": True
                    }
                    
                except sr.WaitTimeoutError:
                    self.logger.warning("Timeout reached - No speech detected")
                    print("❌ No speech detected. Please try again.")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Recording error: {e}")
            return None
                
    def check_microphone(self) -> bool:
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            return True
        except Exception as e:
            self.logger.error(f"Erreur de microphone : {e}")
            return False
                