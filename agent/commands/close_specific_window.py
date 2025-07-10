"""
Command handler to close a specific window by name
"""
import logging
import time
import ctypes
from ctypes import wintypes
import re

logger = logging.getLogger("game-agent")

# Windows API constants
WM_CLOSE = 0x0010

# Load user32.dll for Windows API access
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Define LRESULT type (missing in some Python versions)
if not hasattr(wintypes, 'LRESULT'):
    wintypes.LRESULT = ctypes.c_long

# Define required Windows API functions
EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM), wintypes.LPARAM]
EnumWindows.restype = wintypes.BOOL

GetWindowText = user32.GetWindowTextW
GetWindowText.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
GetWindowText.restype = ctypes.c_int

IsWindowVisible = user32.IsWindowVisible
IsWindowVisible.argtypes = [wintypes.HWND]
IsWindowVisible.restype = wintypes.BOOL

SendMessage = user32.SendMessageW
SendMessage.argtypes = [wintypes.HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM]
SendMessage.restype = wintypes.LRESULT

def find_window_by_name(pattern):
    """
    Find windows that match the given pattern
    Returns a list of (window handle, window title) tuples
    """
    result = []
    pattern = pattern.lower()
    
    def enum_windows_callback(hwnd, lparam):
        if IsWindowVisible(hwnd):
            length = 1024
            buff = ctypes.create_unicode_buffer(length)
            GetWindowText(hwnd, buff, length)
            window_title = buff.value
            if window_title and pattern in window_title.lower():
                result.append((hwnd, window_title))
        return True
    
    EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)(enum_windows_callback), 0)
    return result

def close_window(hwnd):
    """
    Close a window by sending WM_CLOSE message
    """
    SendMessage(hwnd, WM_CLOSE, 0, 0)

def extract_window_name(command_text):
    """
    Extract window name from command text
    Examples:
    - "close chrome window" -> "chrome"
    - "close the discord app" -> "discord"
    - "close spotify please" -> "spotify"
    """
    # Common patterns for window closing commands
    patterns = [
        r"close\s+(?:the\s+)?(.+?)(?:\s+window|\s+app|\s+application)?$",
        r"close\s+(?:the\s+)?(.+?)(?:\s+please|\s+now)?$"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command_text.lower())
        if match:
            return match.group(1).strip()
    
    # If no pattern matches, use words after "close"
    words = command_text.lower().split()
    if "close" in words:
        close_index = words.index("close")
        if close_index < len(words) - 1:
            # Return everything after "close" as the window name
            return " ".join(words[close_index + 1:])
    
    return None

def execute(**kwargs):
    """
    Close a specific window by name
    """
    try:
        command_text = kwargs.get("command_text", "")
        logger.info(f"Executing command: close specific window - '{command_text}'")
        
        # Extract window name from command
        window_name = extract_window_name(command_text)
        
        if not window_name:
            return "Could not determine which window to close"
        
        logger.info(f"Looking for windows matching: '{window_name}'")
        
        # Find matching windows
        matching_windows = find_window_by_name(window_name)
        
        if not matching_windows:
            return f"No windows found matching '{window_name}'"
        
        # Close the first matching window
        hwnd, title = matching_windows[0]
        logger.info(f"Closing window: '{title}' (handle: {hwnd})")
        close_window(hwnd)
        
        # Brief pause to let the window close
        time.sleep(0.2)
        
        return f"Closed window: {title}"
    
    except Exception as e:
        logger.error(f"Error in close_specific_window command: {e}")
        return f"Failed to close window: {e}"
