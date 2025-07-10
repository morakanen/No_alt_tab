import speech_recognition as sr
import time
import sys

def test_microphone():
    """Test if the microphone is working and list available microphones"""
    print("Testing microphone availability...")
    
    try:
        # Get list of microphone names
        mic_list = sr.Microphone.list_microphone_names()
        print(f"Available microphones ({len(mic_list)}):")
        for i, mic_name in enumerate(mic_list):
            print(f"  {i}: {mic_name}")
        
        if len(mic_list) == 0:
            print("No microphones found! Please check your microphone connection.")
            return False
            
        print("\nDefault microphone should be working.")
        return True
    except Exception as e:
        print(f"Error checking microphones: {e}")
        return False

def test_speech_recognition(duration=5, verbose=True):
    """
    Detailed test function for speech recognition with diagnostics.
    
    Args:
        duration: How long to listen for speech (seconds)
        verbose: Whether to print detailed diagnostic information
    """
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    
    print("\nSpeech Recognition Test")
    print("======================")
    print(f"This script will listen for {duration} seconds and try to recognize your speech.")
    print("Please speak clearly into your microphone when prompted.")
    
    # Use the default microphone as the audio source
    try:
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise... Please be quiet for a moment.")
            
            # Adjust for ambient noise with detailed feedback
            start_time = time.time()
            if verbose:
                print("Measuring ambient noise levels...")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            if verbose:
                print(f"Ambient noise adjustment completed in {time.time() - start_time:.2f} seconds")
                print(f"Energy threshold set to: {recognizer.energy_threshold}")
            
            print("\nReady! Please speak now...")
            print(f"Listening for {duration} seconds...")
            
            # Listen for audio input with timeout
            try:
                start_time = time.time()
                audio = recognizer.listen(source, timeout=duration)
                listen_time = time.time() - start_time
                
                if verbose:
                    print(f"Audio captured in {listen_time:.2f} seconds")
                    print(f"Audio length: {len(audio.frame_data)} bytes")
                
                print("\nProcessing audio...")
                
                # Try different speech recognition services
                try:
                    # Try Google's speech recognition
                    start_time = time.time()
                    text = recognizer.recognize_google(audio)
                    process_time = time.time() - start_time
                    
                    print(f"Recognition successful! (processed in {process_time:.2f} seconds)")
                    print(f"You said: \"{text}\"")
                    return True, text
                    
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand the audio")
                    print("Possible reasons:")
                    print("  - Speech wasn't clear enough")
                    print("  - Background noise interference")
                    print("  - Microphone volume too low")
                    print("  - No speech detected in the audio")
                    return False, None
                    
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                    print("Please check your internet connection")
                    return False, None
                    
            except sr.WaitTimeoutError:
                print("No speech detected within the timeout period")
                print("Please check if your microphone is working and try speaking louder")
                return False, None
                
    except Exception as e:
        print(f"Error accessing microphone: {e}")
        print("Please check if your microphone is properly connected and not being used by another application")
        return False, None

if __name__ == "__main__":
    print("Speech Recognition Diagnostic Tool")
    print("=================================")
    
    # Test microphone first
    if test_microphone():
        # If microphone is available, test speech recognition
        print("\nPress Enter to start the speech recognition test...")
        input()
        
        # Run the speech recognition test with a longer duration
        test_speech_recognition(duration=7, verbose=True)
    else:
        print("\nPlease fix microphone issues before continuing.")
        
    print("\nTest completed.")
