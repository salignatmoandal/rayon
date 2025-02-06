import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio settings
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# Paths
DATA_DIR = "data"
LOG_DIR = "logs"

# OpenAI settings
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 1000

# Speech Recognition configuration
SPEECH_RECOGNITION_CONFIG = {
    "energy_threshold": 3000,
    "pause_threshold": 0.8,
    "phrase_threshold": 0.3,
    "non_speaking_duration": 0.5,
    "max_attempts": 2,
    "timeout": 15.0
}

# Noise Reduction configuration
NOISE_REDUCTION_CONFIG = {
    "stationary": True,
    "prop_decrease": 0.75,
    "n_jobs": 2
}
