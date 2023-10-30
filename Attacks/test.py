import re

def __parsePortAndProtocol(data):
        for i in range(len(data)):
             service = data[i]
             portAndProtocol = service[0]
             split = portAndProtocol.split("/")
             protocol = split[1]
             port = split[0]
             data[i].insert(0, protocol)
             data[i].insert(0, port)
             data[i].pop(2)

def __parseNMAPToDatatypes(nmapOutput):
        pattern = re.compile(r"[0-9]+/[A-Za-z]+\s+[A-Za-z]+\s+[A-Za-z-]+", re.IGNORECASE)
        matched = pattern.findall(nmapOutput) # This needs testing

        for i in range(len(matched)):
                rawPortStateService = matched[i]
                matched[i] = rawPortStateService.split()
                
        return matched

def __parse(rawdata):
        data = __parseNMAPToDatatypes(rawdata)
        __parsePortAndProtocol(data)
        return data

rawdata = """
Nmap scan report for 192.168.10.111
Host is up (0.0029s latency).
Not shown: 991 closed ports

PORT     STATE SERVICE

21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
139/tcp  open  netbios-ssn
443/tcp  open  https
445/tcp  open  microsoft-ds
873/tcp  open  rsync
3493/tcp open  nut
8080/tcp open  http-proxy
MAC Address: 00:08:9B:8B:F5:EB (ICP Electronics)
"""

result = __parse(rawdata)
print(result)