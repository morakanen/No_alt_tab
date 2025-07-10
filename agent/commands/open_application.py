"""
Command handler to open specific applications by name
"""
import logging
import subprocess
import re
import os
import time
from pathlib import Path

logger = logging.getLogger("game-agent")

# Common application paths and executables
COMMON_APPS = {
    "chrome": {
        "paths": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],
        "aliases": ["google chrome", "chrome browser", "web browser"]
    },
    "firefox": {
        "paths": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ],
        "aliases": ["mozilla firefox", "firefox browser"]
    },
    "spotify": {
        "paths": [
            r"C:\Users\{username}\AppData\Roaming\Spotify\Spotify.exe"
        ],
        "aliases": ["spotify app", "spotify music"]
    },
    "discord": {
        "paths": [
            r"C:\Users\{username}\AppData\Local\Discord\app-1.0.9013\Discord.exe",
            r"C:\Users\{username}\AppData\Local\Discord\Update.exe --processStart Discord.exe"
        ],
        "aliases": ["discord app", "discord chat"]
    },
    "notepad": {
        "paths": [
            r"C:\Windows\System32\notepad.exe"
        ],
        "aliases": ["text editor", "notes"]
    },
    "calculator": {
        "paths": [
            r"C:\Windows\System32\calc.exe"
        ],
        "aliases": ["calc", "windows calculator"]
    }
}

def extract_app_name(command_text):
    """
    Extract application name from command text
    Examples:
    - "open chrome" -> "chrome"
    - "launch spotify" -> "spotify"
    - "start discord app" -> "discord"
    """
    # Common patterns for application opening commands
    patterns = [
        r"open\s+(?:the\s+)?(.+?)(?:\s+app|\s+application)?$",
        r"launch\s+(?:the\s+)?(.+?)(?:\s+app|\s+application)?$",
        r"start\s+(?:the\s+)?(.+?)(?:\s+app|\s+application)?$",
        r"run\s+(?:the\s+)?(.+?)(?:\s+app|\s+application)?$"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command_text.lower())
        if match:
            return match.group(1).strip()
    
    # If no pattern matches, use words after open/launch/start/run
    words = command_text.lower().split()
    for trigger in ["open", "launch", "start", "run"]:
        if trigger in words:
            trigger_index = words.index(trigger)
            if trigger_index < len(words) - 1:
                # Return everything after the trigger word as the app name
                return " ".join(words[trigger_index + 1:])
    
    return None

def find_app_path(app_name):
    """
    Find the executable path for an application
    """
    # Check if app is in our common apps dictionary
    app_name_lower = app_name.lower()
    
    # First check direct matches
    if app_name_lower in COMMON_APPS:
        app_info = COMMON_APPS[app_name_lower]
        username = os.getenv("USERNAME")
        
        for path in app_info["paths"]:
            # Replace username placeholder if present
            actual_path = path.replace("{username}", username)
            if os.path.exists(actual_path):
                return actual_path
    
    # Check aliases
    for app_key, app_info in COMMON_APPS.items():
        if app_name_lower in app_info["aliases"]:
            username = os.getenv("USERNAME")
            for path in app_info["paths"]:
                actual_path = path.replace("{username}", username)
                if os.path.exists(actual_path):
                    return actual_path
    
    # Try to find in common locations
    common_locations = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.join(os.getenv("LOCALAPPDATA", ""), "Programs"),
        os.path.join(os.getenv("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")
    ]
    
    for location in common_locations:
        if os.path.exists(location):
            # Look for folders matching the app name
            for root, dirs, files in os.walk(location, topdown=True, followlinks=False):
                # Limit depth to avoid excessive searching
                if root.count(os.sep) - location.count(os.sep) > 2:
                    dirs[:] = []  # Don't go deeper
                    continue
                
                # Check if any folder name contains our app name
                for dir_name in dirs:
                    if app_name_lower in dir_name.lower():
                        # Look for executable in this folder
                        app_dir = os.path.join(root, dir_name)
                        for file in os.listdir(app_dir):
                            if file.lower().endswith(".exe") and (
                                app_name_lower in file.lower() or 
                                file.lower() == "launcher.exe" or
                                file.lower() == "app.exe"
                            ):
                                return os.path.join(app_dir, file)
    
    # Not found in common locations
    return None

def execute(command_text="", **kwargs):
    """
    Open a specific application by name
    """
    try:
        logger.info(f"Executing command: open application - '{command_text}'")
        
        # Extract application name from command
        app_name = extract_app_name(command_text)
        
        if not app_name:
            return "Could not determine which application to open"
        
        logger.info(f"Looking for application: '{app_name}'")
        
        # Find application path
        app_path = find_app_path(app_name)
        
        if not app_path:
            return f"Could not find application '{app_name}'"
        
        # Launch the application
        logger.info(f"Launching application: '{app_path}'")
        subprocess.Popen(app_path)
        
        # Brief pause to let the application start
        time.sleep(0.5)
        
        return f"Opened {app_name}"
    
    except Exception as e:
        logger.error(f"Error in open_application command: {e}")
        return f"Failed to open application: {e}"
