"""
Test script for the command parser
"""
from agent.command_parser import CommandParser

def test_command_parser():
    """
    Test the command parser with various phrases
    """
    parser = CommandParser()
    
    # Test phrases to try
    test_phrases = [
        "stop music",
        "please stop the music",
        "mute game",
        "mute the game sound",
        "take a screenshot",
        "capture the screen",
        "open inventory",
        "show my inventory",
        "close this window",
        "turn up the volume",
        "volume down please",
        "skip to next song",
        "go back to previous track",
        "this is not a command"
    ]
    
    print("Testing Command Parser")
    print("=====================\n")
    
    for phrase in test_phrases:
        print(f"Testing phrase: '{phrase}'")
        handler, confidence = parser.parse_command(phrase)
        
        if handler:
            print(f"✓ Matched to handler: '{handler}' with confidence: {confidence:.2f}")
            # Uncomment to actually execute the command
            # result = parser.execute_command(handler)
            # print(f"  Result: {result}")
        else:
            print(f"✗ No matching command found")
        
        print()

if __name__ == "__main__":
    test_command_parser()
