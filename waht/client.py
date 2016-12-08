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

def send_par(list):
    list = q.Quadro('par', list).jsondumps()
    return list

class Client(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = ip

    def run(self):
        print 'Fazendo requisicao no IP: ', self.ip
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.ip, PORT)
        tcp.connect(dest)
        print 'Conectado com: ', tcp.getsockname

        # manda requisicao da lista de arquivos tem
        j = q.Quadro("pli", None).jsondumps()
        tcp.send(j)

        # recebe a lista e seleciona os arquivos que precisa
        msg = tcp.recv(1024)
        msg = json.loads(msg)

        #se o servidor responder com a lista de arquivos dele
        if msg['tipo'] == 'rli':
            server_files = msg
            print '\tlista que recebi do servidor: ', server_files['dados']
            with open(ARQUIVO_CLIENTE, 'r') as f:
                client_list = f.read().splitlines()
                f.close()

            print '\tarquivos no cliente: ', client_list
            server_list = server_files['dados']

            # compara client_files e server_list, remove o que o cliente ja tiver
            rppitems = list(set(client_list) & set(server_list))
            for t in range(len(rppitems)):
                server_list.remove(rppitems[t])
            #na server_list sobra soh o que o cliente nao tem
            print 'arquivos que o cliente precisa: ', server_list

            #envia uma requisicao de arquivos para o servidor
            par = send_par(server_list)
            tcp.send(par)

        if(msg['tipo'] == 'rar'):
            print "Arquivos chegaram"
            #atualizar arquivos_cliente.txt

        tcp.close()

print 'Iniciando requisicoes...'
for t in range(len(ips)):
    thread = Client(ips[t])
    thread.start()
    threads.append(thread)
    time.sleep(3.5)

for t in threads:
    t.join()