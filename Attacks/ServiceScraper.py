from Attack import Attack
from Operations import Client
import random
import requests

class ServiceScraper(Attack):
    def execute(client: Client.Client):
        client.executeShell("sudo lsof -i -n")