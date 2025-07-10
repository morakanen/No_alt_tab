import speech_recognition as sr

def test_speech_recognition():
    """
    Simple test function to verify that speech recognition is working.
    It will listen for audio input and print the recognized text.
    """
    # Create a recognizer instance
    recognizer = sr.Recognizer()
    
    print("Speech Recognition Test")
    print("======================")
    print("This script will test if your microphone and speech recognition are working.")
    print("When prompted, speak a simple phrase like 'Hello world' into your microphone.")
    print()
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please be quiet for a moment.")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        print("Ready! Please speak now...")
        # Listen for audio input
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing audio...")
            
            # Try to recognize the speech using Google's speech recognition
            try:
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                return True, text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return False, None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return False, None
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period")
            return False, None
        
if __name__ == "__main__":
    test_speech_recognition()
