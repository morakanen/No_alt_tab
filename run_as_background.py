"""
Run the No Alt Tab voice assistant as a background process with system tray icon
"""
import os
import sys
import time
import logging
import threading
import subprocess
import signal
import webbrowser
from pathlib import Path
import pystray
from PIL import Image, ImageDraw
import importlib.util

# Check if required packages are installed
required_packages = ['pystray', 'pillow']
missing_packages = []

for package in required_packages:
    if importlib.util.find_spec(package) is None:
        missing_packages.append(package)

if missing_packages:
    print(f"Installing required packages: {', '.join(missing_packages)}")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
    print("Required packages installed. Restarting script...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'background_service.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('no-alt-tab-background')

# Global variables
agent_process = None
dashboard_url = "http://localhost:5000"
is_running = False

def create_icon():
    """Create a simple icon for the system tray"""
    width = 64
    height = 64
    color1 = (0, 128, 255)  # Blue
    color2 = (255, 255, 255)  # White
    
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    
    # Draw a simple microphone-like shape
    dc.rectangle((24, 16, 40, 40), fill=color2)
    dc.ellipse((20, 8, 44, 24), fill=color2)
    dc.rectangle((28, 40, 36, 52), fill=color2)
    dc.ellipse((20, 48, 44, 56), fill=color2)
    
    return image

def start_agent():
    """Start the No Alt Tab agent process"""
    global agent_process, is_running
    
    if is_running:
        logger.info("Agent is already running")
        return
    
    try:
        logger.info("Starting No Alt Tab agent...")
        
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Start the agent as a subprocess
        agent_process = subprocess.Popen(
            [sys.executable, "-m", "agent.main"],
            cwd=script_dir,
            # Redirect output to log files
            stdout=open(os.path.join(log_dir, 'agent_stdout.log'), 'a'),
            stderr=open(os.path.join(log_dir, 'agent_stderr.log'), 'a'),
            # Don't create a console window
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        
        is_running = True
        logger.info("No Alt Tab agent started with PID: %s", agent_process.pid)
        
        # Wait a moment for the server to start
        time.sleep(2)
    except Exception as e:
        logger.error("Failed to start agent: %s", e)

def stop_agent():
    """Stop the No Alt Tab agent process"""
    global agent_process, is_running
    
    if not is_running:
        logger.info("Agent is not running")
        return
    
    try:
        logger.info("Stopping No Alt Tab agent...")
        
        if agent_process:
            # Try to terminate gracefully first
            if sys.platform == 'win32':
                agent_process.terminate()
            else:
                os.kill(agent_process.pid, signal.SIGTERM)
            
            # Wait for process to terminate
            try:
                agent_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate
                if sys.platform == 'win32':
                    agent_process.kill()
                else:
                    os.kill(agent_process.pid, signal.SIGKILL)
            
            agent_process = None
            is_running = False
            logger.info("No Alt Tab agent stopped")
    except Exception as e:
        logger.error("Failed to stop agent: %s", e)

def open_dashboard():
    """Open the web dashboard in the default browser"""
    try:
        logger.info("Opening dashboard in browser...")
        webbrowser.open(dashboard_url)
    except Exception as e:
        logger.error("Failed to open dashboard: %s", e)

def on_exit(icon):
    """Handle exit from system tray"""
    stop_agent()
    icon.stop()

def setup_autostart():
    """Set up the application to run at Windows startup"""
    try:
        import winreg
        
        # Get the path to the current script
        script_path = os.path.abspath(__file__)
        pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        autostart_command = f'"{pythonw_path}" "{script_path}"'
        
        # Open the registry key for startup programs
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Add the registry value
        winreg.SetValueEx(key, "NoAltTabAssistant", 0, winreg.REG_SZ, autostart_command)
        winreg.CloseKey(key)
        logger.info("Added to Windows startup")
        return True
    except Exception as e:
        logger.error(f"Failed to set up autostart: {e}")
        return False

def remove_autostart():
    """Remove the application from Windows startup"""
    try:
        import winreg
        
        # Open the registry key for startup programs
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        
        # Remove the registry value
        winreg.DeleteValue(key, "NoAltTabAssistant")
        winreg.CloseKey(key)
        logger.info("Removed from Windows startup")
        return True
    except Exception as e:
        logger.error(f"Failed to remove from autostart: {e}")
        return False

def check_autostart():
    """Check if the application is set to run at startup"""
    try:
        import winreg
        
        # Open the registry key for startup programs
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        
        try:
            winreg.QueryValueEx(key, "NoAltTabAssistant")
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            winreg.CloseKey(key)
            return False
    except Exception:
        return False

def run_tray_app():
    """Run the system tray application"""
    # Create the system tray icon
    icon = pystray.Icon(
        "no-alt-tab",
        create_icon(),
        "No Alt Tab Voice Assistant",
        menu=pystray.Menu(
            pystray.MenuItem("Status: Running" if is_running else "Status: Stopped", lambda: None, enabled=False),
            pystray.MenuItem("Start Assistant", start_agent, enabled=lambda item: not is_running),
            pystray.MenuItem("Stop Assistant", stop_agent, enabled=lambda item: is_running),
            pystray.MenuItem("Open Dashboard", open_dashboard),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Run at Startup", 
                lambda item: setup_autostart() if not check_autostart() else remove_autostart(),
                checked=lambda item: check_autostart()
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", on_exit)
        )
    )
    
    # Start the agent automatically when the tray app starts
    start_agent()
    
    # Run the system tray icon
    icon.run()

if __name__ == "__main__":
    # Check if running with pythonw (no console)
    is_pythonw = 'pythonw.exe' in sys.executable.lower()
    
    if not is_pythonw and len(sys.argv) <= 1:
        logger.info("Restarting with pythonw to hide console window...")
        pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        
        if os.path.exists(pythonw_path):
            subprocess.Popen([pythonw_path, __file__, "background"])
            sys.exit(0)
    
    # Run the tray application
    run_tray_app()
