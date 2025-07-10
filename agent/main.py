import time
import logging
import importlib
import os
import json
import pyaudio
import threading
import datetime
from vosk import Model, KaldiRecognizer
from flask import Flask, jsonify
from agent.command_parser import CommandParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("game-agent")

# Initialize Flask for REST API
app = Flask(__name__)
command_logs = []

# Initialize command parser
command_parser = CommandParser()

def process_command(transcript):
    """
    Process a command from the transcript using the command parser
    """
    if not transcript:
        return None
    
    # Log the command
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    command_log = {
        "timestamp": timestamp,
        "transcript": transcript,
        "result": None,
        "command": None,
        "confidence": 0
    }
    
    # Parse the command
    handler_name, confidence = command_parser.parse_command(transcript)
    command_log["command"] = handler_name
    command_log["confidence"] = confidence
    
    if handler_name and confidence > 0.5:  # Only execute if confidence is high enough
        try:
            # Execute the command
            result = command_parser.execute_command(handler_name, command_text=transcript)
            command_log["result"] = result
            command_logs.append(command_log)
            return result
        except Exception as e:
            logger.error(f"Error executing {handler_name} command: {e}")
            command_log["result"] = f"Error: {str(e)}"
            command_logs.append(command_log)
            return None
    else:
        # Log unrecognized commands
        command_log["result"] = "Command not recognized or confidence too low"
        command_logs.append(command_log)
        logger.info(f"No command matched in transcript: {transcript}")
        return None

def download_model():
    """
    Download the Vosk model if it doesn't exist
    """
    import requests
    import zipfile
    import io
    
    model_path = "model"
    model_url = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    
    if not os.path.exists(model_path):
        logger.info(f"Downloading Vosk model from {model_url}")
        logger.info("This may take a few minutes depending on your internet connection...")
        
        response = requests.get(model_url, stream=True)
        if response.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(response.content))
            z.extractall()
            # Rename the extracted folder to 'model'
            extracted_dir = z.namelist()[0].split('/')[0]
            if os.path.exists(extracted_dir) and extracted_dir != model_path:
                os.rename(extracted_dir, model_path)
            logger.info(f"Model downloaded and extracted to {model_path}")
        else:
            logger.error(f"Failed to download model: HTTP {response.status_code}")
            return False
    else:
        logger.info(f"Model already exists at {model_path}")
    
    return True

def listen_with_vosk():
    """
    Continuously listens to the microphone using Vosk for local speech recognition.
    Periodically releases the microphone to allow other applications to use it.
    """
    # Ensure we have the model
    if not os.path.exists("model"):
        if not download_model():
            logger.error("Failed to download speech recognition model. Exiting.")
            return
    
    logger.info("Starting voice command listener with Vosk...")
    
    # Initialize Vosk model
    model = Model("model")
    
    # Configure audio settings
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    # Listening cycle settings
    LISTEN_DURATION = 5  # Listen for 5 seconds
    PAUSE_DURATION = 0.5  # Release mic for 0.5 seconds
    
    print("\n===== No Alt Tab Voice Command Agent =====")
    print("Listening for voice commands... Speak clearly into your microphone.")
    print("Available commands: stop music, mute game, take screenshot, open inventory, close window, volume up/down, next/previous track")
    print("Press Ctrl+C to exit")
    print("Microphone is shared with games - voice commands will work even while gaming")
    print("=========================================\n")
    
    running = True
    
    while running:
        try:
            # Initialize PyAudio for each listening cycle
            p = pyaudio.PyAudio()
            
            # Open microphone stream
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
            
            # Create recognizer
            rec = KaldiRecognizer(model, RATE)
            
            logger.info("Listening for commands...")
            print("Listening...", end="\r")
            
            # Keep track of partial results for better user feedback
            last_partial = ""
            
            # Set the start time for this listening cycle
            start_time = time.time()
            
            # Listen for LISTEN_DURATION seconds
            while time.time() - start_time < LISTEN_DURATION:
                try:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    if len(data) == 0:
                        break
                    
                    # Show partial results for better feedback
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "")
                    if partial_text and partial_text != last_partial:
                        print(f"Hearing: {partial_text}                ", end="\r")
                        last_partial = partial_text
                    
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        transcript = result.get("text", "")
                        
                        if transcript:
                            print(f"\nRecognized: {transcript}")
                            logger.info(f"Raw transcript: {transcript}")
                            
                            # Process the command
                            command_result = process_command(transcript)
                            if command_result:
                                print(f"Result: {command_result}")
                                logger.info(f"Command result: {command_result}")
                            else:
                                print("Command not recognized. Try again.")
                            
                            print("\nListening for next command...")
                
                except KeyboardInterrupt:
                    print("\nStopping voice command listener...")
                    logger.info("Stopping voice command listener...")
                    running = False
                    break
                except Exception as e:
                    logger.error(f"Error processing audio: {e}")
                    time.sleep(0.1)  # Prevent tight loop in case of recurring errors
            
            # Close the stream and release the microphone
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Brief pause to allow other applications to access the microphone
            if running:
                time.sleep(PAUSE_DURATION)
        
        except KeyboardInterrupt:
            print("\nStopping voice command listener...")
            logger.info("Stopping voice command listener...")
            running = False
        except Exception as e:
            logger.error(f"Error in voice command listener: {e}")
            print(f"\nError: {e}")
            time.sleep(1)  # Wait before retrying



# REST API endpoints
@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(command_logs)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

def start_api_server():
    """Start the Flask API server"""
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    logger.info("Game Agent starting up...")
    
    # Start the API server in a separate thread
    api_thread = threading.Thread(target=start_api_server)
    api_thread.daemon = True
    api_thread.start()
    
    # Use Vosk for local speech recognition
    listen_with_vosk()
