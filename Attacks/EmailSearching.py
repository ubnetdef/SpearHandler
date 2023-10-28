#Imports results from a file that was output by Webcrawler.py and search for all the emails in all the webpages/directories found 

import subprocess

from Attack import Attack
class Webcrawling(Attack): 
    def execute(self, WordlistPath, URL):
        # Fuzzes the webapp
        command = ["wfuzz", "-c -z file,"+WordlistPath, "--hc 404", URL+"FUZZ"]

        output_file = "fuzzing.txt"

        try:
            # Run the command and capture the output
            output = subprocess.check_output(command, universal_newlines=True)

            # Write output to a file
            with open(output_file, "w") as file:
                file.write(output)

        except subprocess.CalledProcessError as e:
            print("Error: Command failed with return code", e.returncode)
        except FileNotFoundError:
            print("Error: The specified command was not found")
        return