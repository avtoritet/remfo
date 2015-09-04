# remfo.py - by avtoritet
# Find what process is making a connection to external IP and/or port
# Loops until remote ip/port found or program exited (Ctrl+C)
# Connections in 'TIME_WAIT' state PIDs defaults to 0 - non-gettable
# Program only works on Windows and requires PSTools directory to be in PATH env variable
# Must have access to local computers a.k.a Domain Admin
import sys
import time
from subprocess import check_output

def main(argv):

    # input validation
    if len(argv) != 4:
        print "Usage: python remfo.py <local ip> <remote ip> <remote port>"
        print "Use * for ANY remote IP or remote port"
        sys.exit(1)

    # assign vars
    LOCALIP = argv[1] #'10.222.90.112'
    REMOTEIP = argv[2] #'184.51.112.91'
    REMOTEPORT = argv[3] #'80'
    DELAY = 30 # 30 sec default netcat loop delay

    # printing vars
    ip_print = REMOTEIP
    port_print = REMOTEPORT

    # control * -> <empty> for proper searching
    if REMOTEIP == "*":
        REMOTEIP = ''
        ip_print = 'ANY'

    if REMOTEPORT == "*":
        REMOTEPORT = ''
        port_print = 'ANY'

    # command line args - psexec + netcat call
    shell_args = ['\\\\' + LOCALIP]
    netstat_args = ['netstat', '-ano']

    # psexec/netcat main loop
    while(1):
        netstat_out = check_output(['psexec', shell_args[0], netstat_args[0], netstat_args[1]], shell=True)

        if REMOTEIP+":"+REMOTEPORT in netstat_out:
            break

        time.sleep(DELAY)

    # print all matching connections
    print
    print "=====NETSTAT: " + ip_print + ":" + port_print + " CONNECTIONS====="

    # Split netcat output by lines + grab PID
    for item in netstat_out.splitlines():
        if REMOTEIP+":"+REMOTEPORT in item:
            print item.split()
            pid = item.split()[4] # assign PID
    print "----------------------------------------"

    # Print PID
    print
    print "=====NETSTAT: " + ip_print + ":" + port_print + " PID====="
    print "PID is " + pid
    print "----------------------------------------"


    # command line args - wmic call
    proc_info = ['wmic', 'process', 'where', 'ProcessID='+str(pid), 'get', 'Name,', 'ProcessID,', 'ExecutablePath']

    proc_out = check_output(['psexec', shell_args[0], proc_info[0], proc_info[1], proc_info[2], proc_info[3], proc_info[4],
                             proc_info[5], proc_info[6], proc_info[7]], shell=True)

    # print process info
    print
    print "=====WMIC: " + ip_print + ":" + port_print + " PROCESS INFO====="
    print proc_out
    print "----------------------------------------"


if __name__ == '__main__':
    main(sys.argv)