"""
Command handler to pause music specifically in Spotify
"""
import logging
import subprocess
import os
import time
import ctypes
from ctypes import wintypes
import win32gui
import win32process

logger = logging.getLogger('game-agent')

# Windows API constants
WM_APPCOMMAND = 0x0319
APPCOMMAND_MEDIA_PLAY = 0xE0000
APPCOMMAND_MEDIA_PAUSE = 0xE0001
APPCOMMAND_MEDIA_PLAY_PAUSE = 0xE0014

# Define ULONG_PTR type (missing in some Python versions)
if not hasattr(wintypes, 'ULONG_PTR'):
    if ctypes.sizeof(ctypes.c_void_p) == 8:
        wintypes.ULONG_PTR = ctypes.c_ulonglong
    else:
        wintypes.ULONG_PTR = ctypes.c_ulong

# Load user32.dll for direct Windows API access
user32 = ctypes.WinDLL('user32', use_last_error=True)

def find_spotify_window():
    """
    Find the Spotify window handle
    """
    spotify_hwnd = None
    
    def enum_windows_callback(hwnd, _):
        nonlocal spotify_hwnd
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if "spotify" in window_title.lower():
                spotify_hwnd = hwnd
                return False  # Stop enumeration
        return True
    
    win32gui.EnumWindows(enum_windows_callback, None)
    return spotify_hwnd

def send_command_to_spotify(command):
    """
    Send a media command specifically to the Spotify window
    """
    hwnd = find_spotify_window()
    
    if not hwnd:
        logger.error("Could not find Spotify window")
        return False
    
    # Send command to Spotify window
    try:
        # Don't activate the window, just send the command to it
        user32.SendMessageW(hwnd, WM_APPCOMMAND, 0, command)
        logger.info(f"Sent command {command} to Spotify window")
        return True
    except Exception as e:
        logger.error(f"Failed to send command to Spotify: {e}")
        return False

def execute(command_text="", **kwargs):
    """
    Pause music specifically in Spotify
    
    Args:
        command_text (str): Original command text (not used in this handler)
        **kwargs: Additional arguments (not used)
    """
    try:
        logger.info("Executing command: spotify pause")
        
        # Try to send pause command to Spotify
        if send_command_to_spotify(APPCOMMAND_MEDIA_PAUSE):
            return "Paused music in Spotify"
        else:
            return "Failed to control Spotify"
    except Exception as e:
        logger.error(f"Error in spotify_pause command: {e}")
        return f"Failed to pause Spotify: {e}"
