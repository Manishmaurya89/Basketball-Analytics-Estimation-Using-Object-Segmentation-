FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install requirements before copying the code so this layer is cached
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p input_videos output_videos models

ENTRYPOINT ["python", "main.py"]