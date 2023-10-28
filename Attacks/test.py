import requests

nmapServicesList = requests.get("https://svn.nmap.org/nmap/nmap-services")

print(nmapServicesList)