"""
Test script for music control commands (play and stop)
"""
import time
import logging
from agent.commands import play_music, stop_music

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('test-music-controls')

def test_music_controls():
    """
    Test both play and stop music commands
    """
    print("Testing Music Control Commands")
    print("=============================\n")
    
    # Test play music command
    print("1. Testing PLAY MUSIC command...")
    try:
        result = play_music.execute()
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Wait a few seconds to let music start playing
    print("\n   Waiting 3 seconds for music to start playing...")
    time.sleep(3)
    
    # Test stop music command
    print("\n2. Testing STOP MUSIC command...")
    try:
        result = stop_music.execute()
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nTest complete! Did you hear music start and then stop?")
    print("If not, make sure you have a media player open or browser tab with media.")

if __name__ == "__main__":
    test_music_controls()
