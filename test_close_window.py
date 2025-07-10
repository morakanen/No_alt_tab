"""
Test script for the close_specific_window command
"""
from agent.commands.close_specific_window import find_window_by_name, extract_window_name, execute

def test_window_finder():
    """
    Test the window finder functionality
    """
    print("Testing Window Finder")
    print("====================\n")
    
    # List all visible windows
    print("Currently open windows:")
    all_windows = find_window_by_name("")  # Empty string matches all windows
    
    for i, (hwnd, title) in enumerate(all_windows[:10]):  # Show only first 10 to avoid clutter
        print(f"{i+1}. {title} (handle: {hwnd})")
    
    if len(all_windows) > 10:
        print(f"...and {len(all_windows) - 10} more windows")
    
    print("\nTesting window name extraction:")
    test_commands = [
        "close chrome",
        "close the firefox window",
        "close spotify please",
        "close discord app",
        "close the notepad"
    ]
    
    for cmd in test_commands:
        window_name = extract_window_name(cmd)
        print(f"Command: '{cmd}' -> Window name: '{window_name}'")
    
    # Ask user if they want to test closing a window
    print("\nWould you like to test closing a specific window?")
    print("Enter a window name to close (or press Enter to skip): ", end="")
    window_to_close = input()
    
    if window_to_close:
        print(f"\nLooking for windows matching '{window_to_close}'...")
        matching = find_window_by_name(window_to_close)
        
        if matching:
            print(f"Found {len(matching)} matching windows:")
            for i, (hwnd, title) in enumerate(matching):
                print(f"{i+1}. {title} (handle: {hwnd})")
            
            print("\nWould you like to close the first matching window? (y/n): ", end="")
            confirm = input().lower()
            
            if confirm == 'y':
                result = execute(command_text=f"close {window_to_close}")
                print(f"Result: {result}")
            else:
                print("Window closing cancelled.")
        else:
            print(f"No windows found matching '{window_to_close}'")

if __name__ == "__main__":
    test_window_finder()
