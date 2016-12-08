import time
import threading
import socket
import json
import quadro as q
PORT = 54321            # Porta que o Servidor esta
IPS = '/home/meiski/PycharmProjects/P2P/pcp/files/ips.txt'
ARQUIVO_CLIENTE = '/home/meiski/PycharmProjects/P2P/pcp/files/arquivos_cliente.txt'
threads = []


with open(IPS,'r') as f:
    ips = f.read().splitlines()
    f.close()

class Client(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        print 'Fazendo requisicao no IP: ', self.ip
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.ip, PORT)
        tcp.connect(dest)

        # manda requisicao da lista de arquivos tem
        j = q.Quadro("pli", None).jsondumps()
        tcp.send(j)

        # recebe a lista e seleciona os arquivos que precisa
        server_files = tcp.recv(1024)
        print '\tlista que recebi do servidor: ', server_files
        server_files = json.loads(server_files)

        if server_files['tipo'] == 'rli':
            with open(ARQUIVO_CLIENTE, 'r') as f:
                client_files = f.read().splitlines()
                f.close()

            print '\tarquivos no cliente: ', client_files
            server_list = server_files['dados']

            # compara client_files e server_list, remove o que o cliente ja tiver
            rppitems = list(set(client_files) & set(server_list))
            for t in range(len(rppitems)):
                server_list.remove(rppitems[t])
            #na server_list sobra soh o que o cliente nao tem
            print 'arquivos que o cliente precisa: ', server_list

            # logica pra comparar meus arquivos com o do servidor




        tcp.close()

print 'Iniciando requisicoes...'
for t in range(len(ips)):
    thread = Client(ips[t])
    thread.start()
    threads.append(thread)
    time.sleep(3.5)

for t in threads:
    t.join()