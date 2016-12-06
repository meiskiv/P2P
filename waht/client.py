import time
import threading
import socket
import json

PORT = 54321            # Porta que o Servidor esta

with open('/home/meiski/PycharmProjects/P2P/pcp/files/ips.txt','r') as f:
    ips = f.read()
ips = ips.splitlines()
threads = []


class Client(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.ip = ip
    def run(self):
        print 'Fazendo requisicao no IP: ', self.ip
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.ip, PORT)
        tcp.connect(dest)
        json_string = '{"tipo": "pli", "dados": "None"}' #aqui os dados precisam ser null ou uma string null>como fazer??
        jserial = json.dumps(json_string)
        tcp.send(jserial)
        tcp.close()


print 'iniciando requisicoes'
for t in range(len(ips)):
    thread = Client(ips[t])
    thread.start()
    threads.append(thread)
    time.sleep(3.5)

for t in threads:
    t.join()