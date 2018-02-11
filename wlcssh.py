'''
Passes commands and returns output from Cisco WLC over SSH
Requires Paramiko - www.paramiko.org

Usage: wlcssh.py <wlc_ip> <wlc_user> <wlc_password>

netpacket.net
'''
#Script paramters:
wlc_port = 22
wlc_pause = 0.1
encoding = 'UTF-8'

#WLC TCP port can be changed, protocol remains SSH
#WLC pause = time between command write and output read, 0.1sec minimum recommended, increase for slow links or equipment

__author__ = 'Michal Kowalik'
__version__= '0.1'
__status__ = 'Prototype'

import sys, time, paramiko

def end():
    print('\nUsage: wlcssh.py <wlc_ip> <wlc_user> <wlc_password>')
    sys.exit()

def wlc_connect(ip, username, password):
    fakeuser, fakepass = 'fake', 'fake' #AireOS doesn't use auth parameters passed by Paramiko - CSCve45024
    wlc_init = paramiko.SSHClient()
    wlc_init.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Allow WLC self-signed certificate, not ideal for secure production environments
    try:
        wlc_init.connect(ip, port=wlc_port, username=fakeuser, password=fakepass)
    except IOError:
        print('Error connecting to WLC')
        sys.exit()
    ssh_class = wlc_init.invoke_shell()
    ssh_class.keep_this = wlc_init #Prevents closed socket after function returns
    time.sleep(wlc_pause)
    ssh_class.send(username.encode(encoding)+b'\n')
    time.sleep(wlc_pause)
    ssh_class.send(password.encode(encoding)+b'\n')
    time.sleep(wlc_pause)
    ssh_class.send('config paging disable'+'\n')
    time.sleep(wlc_pause)
    strip_lead = ssh_class.recv(1024).decode('ascii')
    return ssh_class

def get_output(command):
    wlc_session.send(command+'\n')
    time.sleep(wlc_pause)
    output = wlc_session.recv(8192).decode('ascii')
    print(output)
    return

if __name__ == '__main__':
    if len(sys.argv) < 4: end()
    wlc_ip, wlc_user, wlc_pass = sys.argv[1], sys.argv[2], sys.argv[3]
    wlc_session = wlc_connect(wlc_ip, wlc_user, wlc_pass)
    command = 'sh ap summary'
    get_output(command)
