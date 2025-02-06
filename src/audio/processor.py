from typing import Optional
import numpy as np
import noisereduce as nr
import speech_recognition as sr
import logging

class AudioProcessor:
    """
    Process audio input to reduce noise and convert to text.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
    
    def record_audio(self, calibration_duration: int = 5, recording_duration: int = 5) -> Optional[np.ndarray]:
        """
        Record audio from the microphone.
        """
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                print("Calibrating for ambient noise...")
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                print("Recording...")
                audio = self.recognizer.listen(source, timeout=recording_duration)
                print("Recording complete.")
                return audio
            except Exception as e:
                print(f"Error recording audio: {e}")
                return None
    def reduce_noise(self, audio_data: sr.AudioData) -> Optional[sr.AudioData]:
        """
        Reduce noise from the audio.
        Args: 
            audio_data: Audio data to reduce noise from
        Returns:
            Optional[sr.AudioData]: Reduced audio data
        """
        try:
            # Convert audio to numpy array
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            
            # Apply noise reduction
            cleaned_array = nr.reduce_noise(
                y=audio_array,
                sr=audio_data.sample_rate,
                stationary=True
            )
            
            # Reconvert to AudioData
            return sr.AudioData(
                cleaned_array.tobytes(),
                audio_data.sample_rate,
                2  # sample width
            )
        except Exception as e:
            self.logger.error(f"Error reducing noise: {e}")
            return None
            

    
    
                

        
        
