"""
Command handler for decreasing system volume
"""
import logging
import keyboard

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the volume down command by sending volume down key
    """
    logger.info("Executing command: volume down")
    
    try:
        # Send volume down key - works on most Windows systems
        keyboard.press_and_release('volume down')
        logger.info("Sent volume down key")
        
        return "Volume decreased"
    except Exception as e:
        logger.error(f"Failed to execute volume down command: {e}")
        return f"Error decreasing volume: {str(e)}"
