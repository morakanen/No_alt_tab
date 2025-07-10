"""
Test script for Spotify-specific music control commands
"""
import time
import logging
from agent.commands import spotify_play, spotify_pause

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('test-spotify-controls')

def test_spotify_controls():
    """
    Test both play and pause Spotify commands
    """
    print("Testing Spotify-Specific Music Controls")
    print("======================================\n")
    
    # Test play Spotify command
    print("1. Testing PLAY SPOTIFY command...")
    try:
        result = spotify_play.execute()
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Wait a few seconds to let music start playing
    print("\n   Waiting 3 seconds for Spotify to start playing...")
    time.sleep(3)
    
    # Test pause Spotify command
    print("\n2. Testing PAUSE SPOTIFY command...")
    try:
        result = spotify_pause.execute()
        print(f"   Result: {result}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\nTest complete! Did Spotify start playing and then pause?")
    print("If Spotify didn't launch automatically, make sure it's installed on your system.")

if __name__ == "__main__":
    test_spotify_controls()
