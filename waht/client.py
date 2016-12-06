import time
import threading
import socket
import json
import quadro
#import os

PORT = 54321            # Porta que o Servidor esta

with open('/home/user/PycharmProjects/P2P/pcp/files/ips.txt','r') as f:
    ips = f.read()
ips = ips.splitlines()
threads = []


class Client(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip
    def run(self):
        print 'Fazendo requisicao no IP: ', self.ip
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.ip, PORT)
        tcp.connect(dest)
        j = quadro.Quadro("pli", None)
       #j = j.toJson()
        j = json.dumps(j.__dict__)
        tcp.send(j)
        tcp.close()



print 'iniciando requisicoes'
for t in range(len(ips)):
    thread = Client(ips[t])
    thread.start()
    threads.append(thread)
    time.sleep(3.5)

for t in threads:
    t.join()