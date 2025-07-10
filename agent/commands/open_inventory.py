"""
Command handler for opening inventory in games
"""
import logging
import keyboard

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the open inventory command by sending the 'i' key
    which is commonly used in games to open inventory
    """
    logger.info("Executing command: open inventory")
    
    try:
        # Most games use 'i' key for inventory
        keyboard.press_and_release('i')
        logger.info("Sent 'i' key to open inventory")
        return "Inventory opened"
    except Exception as e:
        logger.error(f"Failed to execute open inventory command: {e}")
        return f"Error opening inventory: {str(e)}"
