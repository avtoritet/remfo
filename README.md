# remfo
Find out what process and executable connecting to remote IP on your domain
~by avtoritet

Usage example: python remfo.py 10.125.15.90 204.55.18.20 8070

Find what process is making a connection to external IP and/or port
Loops until remote ip/port found or program is exited (Ctrl+C)
Connections in 'TIME_WAIT' state PIDs defaults to 0 - non-gettable
Program only works on Windows and requires PSTools directory to be in PATH env variable
Must have access to computers on that domain a.k.a Domain Admin privileges
