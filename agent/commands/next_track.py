"""
Command handler for skipping to the next music track
"""
import logging
import keyboard

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the next track command by sending next track media key
    """
    logger.info("Executing command: next track")
    
    try:
        # Send next track media key - works with most media players
        keyboard.press_and_release('next track')
        logger.info("Sent next track media key")
        
        return "Skipped to next track"
    except Exception as e:
        logger.error(f"Failed to execute next track command: {e}")
        return f"Error skipping track: {str(e)}"
