# app/Dockerfile

# Récupère l'image pythonXXX depuis le cloud docker 
FROM python:3.9-slim

# Choix du dossier courrant sur le conteneur
WORKDIR /app


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

#RUN git clone https://github.com/MTES-MCT/qualicharge-geoviz-public .

COPY . .

#MOUNT src src
#MOUNT data data

RUN pip3 install -r install/requirements.txt

# Exposition du port Streamlit sur le conteneur
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]