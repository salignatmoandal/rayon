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
            # Conversion en array numpy
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            
            # Paramètres optimisés pour la réduction du bruit
            cleaned_array = nr.reduce_noise(
                y=audio_array,
                sr=audio_data.sample_rate,
                stationary=True,
                prop_decrease=0.75,
                n_jobs=2  # Parallélisation
            )
            
            # Normalisation du volume
            cleaned_array = np.int16(cleaned_array * (32767/max(abs(cleaned_array))))
            
            return sr.AudioData(
                cleaned_array.tobytes(),
                audio_data.sample_rate,
                2
            )
        except Exception as e:
            self.logger.error(f"Error reducing noise: {e}")
            return None
            

    
    
                

        
        
