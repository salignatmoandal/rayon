
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