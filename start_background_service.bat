@echo off
echo Starting No Alt Tab Voice Assistant in background mode...
start /b pythonw.exe run_as_background.py
echo Service started! You can now close this window.
timeout /t 5
