"""
Command handler for stopping music in games or media players
"""
import logging
import keyboard
import time
import ctypes
from ctypes import wintypes

logger = logging.getLogger('game-agent')

# Windows API constants for media keys
VK_MEDIA_PLAY_PAUSE = 0xB3
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

# Define ULONG_PTR type (missing in some Python versions)
if not hasattr(wintypes, 'ULONG_PTR'):
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        wintypes.ULONG_PTR = ctypes.c_ulonglong
    else:
        wintypes.ULONG_PTR = ctypes.c_ulong

# Load user32.dll for direct Windows API access
user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.keybd_event.argtypes = [wintypes.BYTE, wintypes.BYTE, wintypes.DWORD, wintypes.ULONG_PTR]

def send_media_key():
    """
    Sends media play/pause key using direct Windows API calls
    This has better compatibility with games than the keyboard module
    """
    # Press the key
    user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
    # Release the key
    user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

def execute(command_text="", **kwargs):
    """
    Sends media play/pause key to toggle music playback.
    Uses both direct Windows API and keyboard module for maximum compatibility.
    
    Args:
        command_text (str): Original command text (not used in this handler)
        **kwargs: Additional arguments (not used)
    """
    try:
        logger.info("Executing command: stop music")
        
        # Try Windows API method first (works better with games)
        try:
            send_media_key()
            logger.info("Sent media play/pause via Windows API")
        except Exception as api_error:
            logger.warning(f"Windows API method failed: {api_error}, falling back to keyboard module")
            # Fall back to keyboard module
            keyboard.press_and_release('play/pause media')
            logger.info("Sent media play/pause via keyboard module")
        
        # Brief pause to ensure the key is registered
        time.sleep(0.1)
        
        return "Music playback toggled"
    except Exception as e:
        logger.error(f"Error in stop_music command: {e}")
        return f"Failed to toggle music: {e}"
