from typing import Optional
import numpy as np
import noisereduce as nr
import speech_recognition as sr
import logging
import os

class AudioProcessor:
    """
    Processes audio input to reduce noise and prepare it for recognition.
    
    This class attempts to initialize a microphone for live audio recording.
    In environments where no microphone is available (e.g., Docker on macOS),
    it gracefully falls back to using a test audio file.
    """
    def __init__(self, use_microphone: bool = True, fallback_audio_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        
        # Option to force fallback (use_microphone=False) if no live audio input is expected.
        if use_microphone:
            try:
                self.microphone = sr.Microphone()
                self.logger.info("Microphone successfully initialized.")
            except OSError as e:
                self.logger.error("No microphone available, switching to fallback mode. Error: %s", e)
                self.microphone = None
        else:
            self.logger.info("Microphone usage disabled. Using fallback audio.")
            self.microphone = None

        # If a fallback audio file is provided, check that it exists.
        if fallback_audio_path and os.path.exists(fallback_audio_path):
            self.fallback_audio_path = fallback_audio_path
            self.logger.info("Fallback audio file set: %s", fallback_audio_path)
        else:
            # If not provided or doesn't exist, set to None.
            self.fallback_audio_path = None
            if fallback_audio_path:
                self.logger.warning("Fallback audio file not found: %s", fallback_audio_path)

    def record_audio(self, calibration_duration: int = 5, recording_duration: int = 5) -> Optional[sr.AudioData]:
        """
        Records audio from the microphone if available; otherwise, uses a fallback audio file.
        
        Args:
            calibration_duration (int): Duration (in seconds) for ambient noise calibration.
            recording_duration (int): Maximum duration (in seconds) to wait for audio input.
            
        Returns:
            Optional[sr.AudioData]: The recorded audio data or None if recording fails.
        """
        # If a microphone is available, attempt live recording.
        if self.microphone:
            try:
                self.logger.info("Calibrating microphone for ambient noise...")
                with self.microphone as source:
                    # Adjust for ambient noise for the specified duration
                    self.recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                    self.logger.info("Recording live audio...")
                    audio = self.recognizer.listen(source, timeout=recording_duration)
                    self.logger.info("Recording complete.")
                    return audio
            except Exception as e:
                self.logger.error("Error recording live audio: %s", e)
                return None
        else:
            # If no microphone is available, try to use a fallback audio file.
            if self.fallback_audio_path:
                try:
                    self.logger.info("Using fallback audio file: %s", self.fallback_audio_path)
                    with sr.AudioFile(self.fallback_audio_path) as source:
                        audio = self.recognizer.record(source)
                        self.logger.info("Fallback audio loaded successfully.")
                        return audio
                except Exception as e:
                    self.logger.error("Error loading fallback audio file: %s", e)
                    return None
            else:
                self.logger.error("No microphone available and no fallback audio file provided.")
                return None

    def reduce_noise(self, audio_data: sr.AudioData) -> Optional[sr.AudioData]:
        """
        Reduces background noise from the provided audio data.
        
        Args:
            audio_data (sr.AudioData): The raw audio data to process.
            
        Returns:
            Optional[sr.AudioData]: The noise-reduced audio data, or None if processing fails.
        """
        try:
            # Convert raw audio data to a NumPy array of type int16
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            
            # Apply noise reduction with optimized parameters
            cleaned_array = nr.reduce_noise(
                y=audio_array,
                sr=audio_data.sample_rate,
                stationary=True,
                prop_decrease=0.75,
                n_jobs=2  # Use parallel processing if available
            )
            
            # Normalize the volume of the cleaned audio
            max_val = np.max(np.abs(cleaned_array))
            if max_val == 0:
                self.logger.warning("Cleaned audio array is silent.")
                return audio_data  # Return original if normalization fails
            cleaned_array = np.int16(cleaned_array * (32767 / max_val))
            
            # Return a new AudioData instance with the cleaned audio
            return sr.AudioData(
                cleaned_array.tobytes(),
                audio_data.sample_rate,
                2  # Assuming 2 bytes per sample (16-bit audio)
            )
        except Exception as e:
            self.logger.error("Error reducing noise: %s", e)
            return None