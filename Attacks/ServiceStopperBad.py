from Attack import Attack
from Operations import Client
import random
import requests

class ServiceStopper(Attack):
    def removeCommentLines(response: requests.Response):
        removedCommentLines = ""
        for line in response.iter_lines(decode_unicode=True):
            if str(line[0]) == "#":
                continue

            removedCommentLines += str(line) + "\t"
        return removedCommentLines

    def formatAsList(response):
        splitResponse = response.split("\t")
        print(splitResponse)
        return splitResponse

    def formatResponse(response: requests.Response):
        text = removeCommentLines(response)
        text = formatAsList(text)
        return text

    nmapServicesResponse = requests.get("https://svn.nmap.org/nmap/nmap-services")
    nmapServicesFormatted = formatResponse(nmapServicesResponse)