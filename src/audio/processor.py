
from typing import Optional
import numpy as np
import noisereduce as nr
import speech_recognition as sr

class AudioProcessor:
    """
    Process audio input to reduce noise and convert to text.
    """
    def __init__(self):
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
    def reduce_noise(self, audio_data: sr.AudioData) -> np.ndarray:
        """
        Reduce noise from the audio.
        Args: 
            audio_data: Audio data to reduce noise from
        Returns:
            np.ndarray: Audio data with reduced noise
        """
        try:
            # Convert audio to numpy array
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            
            # Apply noise reduction
            return nr.reduce_noise(
                y=audio_array,
                sr=audio_data.sample_rate,
                stationary=True
            )
            
        except Exception as e:
            print(f"Error reducing noise: {e}")
            return None
            

    
    
                

        
        
