import os
import sys
import json
import wave
import pyaudio
import requests
import zipfile
import io
from vosk import Model, KaldiRecognizer

def download_model():
    """Download the Vosk model if it doesn't exist"""
    model_path = "model"
    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    
    if not os.path.exists(model_path):
        print(f"Downloading Vosk model from {model_url}")
        print("This may take a few minutes depending on your internet connection...")
        
        response = requests.get(model_url, stream=True)
        if response.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall()
            # Rename the extracted folder to 'model'
            extracted_dir = z.namelist()[0].split('/')[0]
            if os.path.exists(extracted_dir) and extracted_dir != model_path:
                os.rename(extracted_dir, model_path)
            print(f"Model downloaded and extracted to {model_path}")
        else:
            print(f"Failed to download model: HTTP {response.status_code}")
            return False
    else:
        print(f"Model already exists at {model_path}")
    
    return True

def test_vosk_recognition():
    """Test speech recognition using Vosk"""
    if not download_model():
        print("Failed to download the model. Exiting.")
        return
    
    print("\nInitializing Vosk speech recognition...")
    model = Model("model")
    
    # Configure audio settings
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    
    print("\nVosk Speech Recognition Test")
    print("===========================")
    print("This test will use Vosk for local, offline speech recognition.")
    print("When prompted, speak clearly into your microphone.")
    print("Press Ctrl+C to stop the test.")
    
    try:
        # Open microphone stream
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        # Create recognizer
        rec = KaldiRecognizer(model, RATE)
        
        print("\nListening... (Press Ctrl+C to stop)")
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            if len(data) == 0:
                break
            
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if result.get("text", ""):
                    print(f"Recognized: {result['text']}")
            else:
                partial = json.loads(rec.PartialResult())
                if partial.get("partial", ""):
                    print(f"Partial: {partial['partial']}", end="\r")
    
    except KeyboardInterrupt:
        print("\n\nStopping speech recognition.")
    
    except Exception as e:
        print(f"\nError during speech recognition: {e}")
    
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        p.terminate()
        print("\nTest completed.")

if __name__ == "__main__":
    print("Vosk Local Speech Recognition Test")
    print("=================================")
    test_vosk_recognition()
