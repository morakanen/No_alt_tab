"""
Command handler for closing windows
"""
import logging
import keyboard
import win32gui
import win32con

logger = logging.getLogger("game-agent")

def execute(**kwargs):
    """
    Execute the close window command by sending Alt+F4 to close the active window
    """
    logger.info("Executing command: close window")
    
    try:
        # Method 1: Use Alt+F4 to close the active window
        keyboard.press_and_release('alt+f4')
        logger.info("Sent Alt+F4 to close active window")
        
        # Method 2: Alternative approach using Windows API
        # Get the handle of the foreground window
        # hwnd = win32gui.GetForegroundWindow()
        # if hwnd:
        #     # Send WM_CLOSE message to the window
        #     win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        #     logger.info(f"Sent close message to window handle {hwnd}")
        
        return "Window close command sent"
    except Exception as e:
        logger.error(f"Failed to execute close window command: {e}")
        return f"Error closing window: {str(e)}"
