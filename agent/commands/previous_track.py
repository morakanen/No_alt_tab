"""
Command handler for going back to the previous music track
"""
import logging
import keyboard

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the previous track command by sending previous track media key
    """
    logger.info("Executing command: previous track")
    
    try:
        # Send previous track media key - works with most media players
        keyboard.press_and_release('previous track')
        logger.info("Sent previous track media key")
        
        return "Returned to previous track"
    except Exception as e:
        logger.error(f"Failed to execute previous track command: {e}")
        return f"Error returning to previous track: {str(e)}"
