from Attack import Attack
from Operations import Client
import random
import requests

# Different methods of serice stopper, future
# - Stop via previous NMAP results & known services
# - Grapping services running on ports (this implementation) (requires sudo)
# - NMAP self
# - 

class ServiceStopper(Attack):
    def execute(client: Client.Client):
        client.executeShell("systemctl stop %s" % ServiceName)