FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for PyAudio and X11 for keyboard control
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    libx11-dev \
    libxtst-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download Vosk model during build
RUN mkdir -p /app/model && \
    python -c "import requests; import zipfile; import io; \
    print('Downloading Vosk model...'); \
    response = requests.get('https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'); \
    z = zipfile.ZipFile(io.BytesIO(response.content)); \
    z.extractall(); \
    import os; import shutil; \
    extracted_dir = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith('vosk-model')][0]; \
    for item in os.listdir(extracted_dir): \
        s = os.path.join(extracted_dir, item); \
        d = os.path.join('model', item); \
        if os.path.isdir(s): \
            shutil.copytree(s, d); \
        else: \
            shutil.copy2(s, d); \
    print('Model downloaded and extracted to /app/model');"

# Expose port for Flask API
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app

# Run the agent
CMD ["python", "-m", "agent.main"]
