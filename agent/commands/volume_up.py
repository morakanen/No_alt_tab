"""
Command handler for increasing system volume
"""
import logging
import keyboard

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the volume up command by sending volume up key
    """
    logger.info("Executing command: volume up")
    
    try:
        # Send volume up key - works on most Windows systems
        keyboard.press_and_release('volume up')
        logger.info("Sent volume up key")
        
        return "Volume increased"
    except Exception as e:
        logger.error(f"Failed to execute volume up command: {e}")
        return f"Error increasing volume: {str(e)}"
