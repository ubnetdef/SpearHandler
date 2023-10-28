from Attack import Attack
from Operations import Client
import random
import requests

class ServiceStopper(Attack):
    def stopRandomService(services):
        service = random.choice(services)

    def __getPopularServices(client: Client.Client):
        nmapServicesList = requests.get("https://svn.nmap.org/nmap/nmap-services")
        
        #response = client.executeShell("netstat -ano | grep [Port Number]")

    def execute(client: Client.Client):
        services = getPopularServices(client);
        stopRandomService(services)