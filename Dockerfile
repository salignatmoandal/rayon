# Image de base avec support audio
FROM python:3.9-slim

# Installation des dépendances système avec conservation des logs
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    gcc \
    vim \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail
WORKDIR /app

# Création des répertoires pour les logs
RUN mkdir -p /app/logs /app/output

# Copie des fichiers nécessaires
COPY requirements.txt .
COPY src/ ./src/
COPY setup.py .

# Installation des dépendances Python avec logs détaillés
RUN pip install --no-cache-dir -r requirements.txt 2>&1 | tee /app/logs/pip_install.log
RUN python -m spacy download fr_core_news_sm 2>&1 | tee /app/logs/spacy_install.log

# Variables d'environnement
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV LOG_LEVEL=DEBUG

# Script de démarrage pour la gestion des logs
COPY <<EOF /app/start.sh
#!/bin/bash
echo "Starting application with logging..."
python src/main.py 2>&1 | tee /app/logs/app.log
EOF

RUN chmod +x /app/start.sh

# Point d'entrée
CMD ["/app/start.sh"]
# Point d'entrée
