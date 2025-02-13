from typing import Optional, Dict, Any
import speech_recognition as sr
import logging
from audio.recorder import AudioRecorder
from audio.processor import AudioProcessor

class SpeechRecognizer:
    """
    Speech recognition class that records audio, processes it, and converts it to text.
    This version is designed to handle cases where no microphone is available by using a fallback audio file.
    """
    
    def __init__(self):
        # Initialize audio recorder and processor modules
        self.audio_recorder = AudioRecorder()
        self.audio_processor = AudioProcessor()
        # Initialize the speech recognition engine
        self.recognizer = sr.Recognizer()
        # Configure logger for debugging and error reporting
        self.logger = logging.getLogger(__name__)
        
        # Adjust recognition parameters for better performance
        self.recognizer.energy_threshold = 3000         # Lower sensitivity to filter out background noise
        self.recognizer.dynamic_energy_threshold = True   # Enable dynamic adjustment of the energy threshold
        self.recognizer.pause_threshold = 0.8             # Seconds of pause before the phrase is considered complete
        self.recognizer.phrase_threshold = 0.3            # Minimum length of a phrase
        self.recognizer.non_speaking_duration = 0.5       # Duration (in seconds) to ignore silence at the beginning
        
        # Attempt to initialize the microphone; if unavailable, set it to None for fallback mode
        try:
            self.microphone = sr.Microphone()
        except OSError as e:
            self.logger.error("No input device detected, switching to simulation mode using a test audio file.")
            self.microphone = None  # Fallback: later use a test audio file for recognition

    def convert_to_text(self, audio_data: sr.AudioData) -> Optional[str]:
        """
        Convert audio data to text using Google's speech recognition API.
        
        Args:
            audio_data (sr.AudioData): The audio data to be recognized.
            
        Returns:
            Optional[str]: The recognized text, or None if recognition fails.
        """
        try:
            # Attempt to convert audio data to text in French
            return self.recognizer.recognize_google(
                audio_data, 
                language="fr-FR"
            )
        except sr.UnknownValueError:
            # Occurs when the speech is unintelligible
            self.logger.warning("Unable to recognize speech")
            return None
        except sr.RequestError as e:
            # Occurs when the API is unreachable or unresponsive
            self.logger.error(f"API unavailable or unresponsive: {e}")
            return None

    def listen_and_convert(self) -> Optional[Dict[str, Any]]:
        """
        Record audio (via microphone or fallback to a test audio file), process it (e.g., noise reduction),
        and convert the processed audio to text.
        
        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the recognized text, duration, channel information,
            and a confidence level. Returns None if the process fails.
        """
        try:
            # Start calibration of the audio recorder with user feedback
            self.logger.info("Starting calibration...")
            if not self.audio_recorder.calibrate():
                self.logger.error("Calibration failed")
                return None
                
            # Attempt to record audio using voice activity detection (VAD)
            self.logger.info("Listening...")
            # If a microphone is available, record from it; otherwise, fallback to using a test audio file.
            if self.microphone:
                recording = self.audio_recorder.record_with_vad(
                    MIN_DURATION=1.0,
                    MAX_DURATION=15.0
                )
            else:
                self.logger.info("No microphone available; using test audio file for recognition.")
                # This assumes you have a test audio file named "audio_test.wav" in your working directory
                with sr.AudioFile("audio_test.wav") as source:
                    audio_data = self.recognizer.record(source)
                # Create a dummy recording dictionary to mimic the structure from a live recording
                recording = {
                    "audio_data": audio_data,
                    "duration": 0,     # Duration is not measured here
                    "channels": 1      # Assuming mono channel for test audio
                }
            
            if not recording:
                self.logger.error("No audio recorded")
                return None
                
            # Process the recorded audio to reduce background noise
            self.logger.info("Processing audio...")
            cleaned_audio = self.audio_processor.reduce_noise(recording["audio_data"])
            if not cleaned_audio:
                self.logger.error("Audio cleaning failed")
                return None
                
            # Attempt speech recognition, trying twice with slightly different conditions if needed
            for attempt in range(2):
                try:
                    text = self.recognizer.recognize_google(
                        cleaned_audio,
                        language="fr-FR",
                        show_all=False
                    )
                    if text:
                        # Return recognized text along with additional metadata
                        return {
                            "text": text,
                            "audio_duration": recording["duration"],
                            "channels": recording["channels"],
                            "confidence": "high" if attempt == 0 else "medium"
                        }
                except sr.UnknownValueError:
                    self.logger.warning(f"Attempt {attempt + 1} failed")
                    continue
                    
            # If no recognition was successful, return None
            return None
            
        except Exception as e:
            # Catch any unexpected errors during the process
            self.logger.error(f"Error in speech recognition: {e}")
            return None