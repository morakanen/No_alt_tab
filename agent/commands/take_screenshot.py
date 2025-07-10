"""
Command handler for taking screenshots in games
"""
import logging
import time
import os
import keyboard

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the take screenshot command using Windows screenshot shortcuts
    """
    logger.info("Executing command: take screenshot")
    
    try:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.path.expanduser("~"), "Pictures", "NoAltTab_Screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Windows screenshot shortcut (Windows+PrintScreen)
        # This automatically saves to Pictures folder on Windows 10+
        keyboard.press_and_release('win+print screen')
        logger.info("Sent Win+PrintScreen key combination")
        
        # Alternative: Some games have their own screenshot key
        # keyboard.press_and_release('f12')  # Common in Steam games
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot-{timestamp}.png"
        
        return f"Screenshot taken using system shortcut"
    except Exception as e:
        logger.error(f"Failed to execute take screenshot command: {e}")
        return f"Error taking screenshot: {str(e)}"
