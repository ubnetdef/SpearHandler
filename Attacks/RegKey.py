#Change Program Name and Path otherwise works

import os
import sys
import ctypes
import winreg

def add_program_to_startup(program_name, program_path):
    try:
        # Open the registry key for startup programs
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)

        # Set the registry value with the program name and path
        winreg.SetValueEx(key, program_name, 0, winreg.REG_SZ, program_path)

        # Close the registry key
        winreg.CloseKey(key)

        print(f"Added '{program_name}' to startup with path: {program_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if ctypes.windll.shell32.IsUserAnAdmin() != 1:
        # Check if the script is running with admin privileges, if not, restart it with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        # Add the Windows Calculator to startup
        program_name = "Calculator"
        program_path = r"C:\Windows\System32\calc.exe"  # Path to the Calculator executable

        add_program_to_startup(program_name, program_path)