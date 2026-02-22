FROM python:3.11-slim

# Meta-data pour l'entreprise
LABEL maintainer="camrail-industrial-data-platform"
LABEL version="2.0-Production"

# Setup OS
WORKDIR /app
RUN apt-get update && apt-get install -y gcc sqlite3 libsqlite3-dev

# Installation Python Dependencies (Cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du Code Source
COPY . .

# Ports pour l'API Flask (5000) et le Dashboard Streamlit (8501)
EXPOSE 5000
EXPOSE 8501

# Scripts Init (API par défaut, un bash script pourrait lancer Streamlit avec)
CMD ["python", "api/api.py"]
