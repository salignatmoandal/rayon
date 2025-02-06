# Image de base avec support audio
FROM python:3.9-slim

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt .
COPY src/ ./src/
COPY setup.py .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download fr_core_news_sm

# Variables d'environnement
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Point d'entrée
CMD ["python", "src/main.py"]