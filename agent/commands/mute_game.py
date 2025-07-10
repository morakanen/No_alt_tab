"""
Command handler for muting game audio
"""
import logging
import keyboard

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the mute game command by sending volume mute key
    """
    logger.info("Executing command: mute game")
    
    try:
        # Send volume mute key - works on most Windows systems
        keyboard.press_and_release('volume mute')
        logger.info("Sent volume mute key")
        
        return "System audio muted/unmuted"
    except Exception as e:
        logger.error(f"Failed to execute mute game command: {e}")
        return f"Error muting audio: {str(e)}"
