import time
import threading
import socket
import json
import quadro as q
from socket import error as SocketError
import errno
import base64
import os

PORT = 54321            # Porta que o Servidor esta
IPS = os.path.realpath('files/ips.txt')
LISTA_ARQ = os.path.realpath('files/lista_arquivos.txt')
ARQ = os.path.realpath('files')

threads = []

with open(IPS, 'r') as f:
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
        print '\nFazendo requisicao no IP: ', self.ip
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (self.ip, PORT)
        try:
            tcp.connect(dest)
        except SocketError as e:
            print 'Erro na conexao, exacute novamente. \nErro: ', e
        print 'Conectado com: ', tcp.getsockname

        # manda requisicao da lista de arquivos tem
        j = q.Quadro("pli", None).jsondumps()
        tcp.send(j)

        # recebe a lista e seleciona os arquivos que precisa
        msg = tcp.recv(1024)
        msg = json.loads(msg)


        # while True:
        # se o servidor responder com a lista de arquivos dele
        if msg['tipo'] == 'rli':
            server_files = msg['dados']
            print '\tlista que recebi do servidor: ', server_files
            with open(LISTA_ARQ, 'r') as f:
                client_list = f.read().splitlines()
                f.close()

            print '\tarquivos no cliente: ', client_list
            server_list = server_files

            # compara client_files e server_list, remove o que o cliente ja tiver
            rppitems = list(set(client_list) & set(server_list))
            for t in range(len(rppitems)):
                server_list.remove(rppitems[t])
            #na server_list sobra soh o que o cliente nao tem
            print 'arquivos que o cliente precisa: ', server_list

            #envia uma requisicao de arquivos para o servidor
            par = send_par(server_list)
            try:
                tcp.send(par)
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    raise
                pass
                print 'except SocketError NO PAR'

        for r in range(len(server_list)):
            msg = tcp.recv(1024)
            msg = json.loads(msg)
            print 'msg: ', msg['dados']

            # recebe arquivos que estavam faltando
            if msg['tipo'] == 'rar':
                arquivos = msg['dados']
                print 'Recebendo arquivos: ', arquivos

                # crio txts pra armazenar as coisas
                f = open(ARQ + '/' + arquivos[0], 'a')
                f.write(base64.b64decode(arquivos[1]))
                f.close()

                # atualizar lista_arquivos.txt
                f= open(LISTA_ARQ, 'a')
                f.write('\n' + arquivos[0])
                f.close()


        tcp.close()


print 'Iniciando requisicoes...'
for t in range(len(ips)):
    thread = Client(ips[t])
    thread.start()
    threads.append(thread)
    time.sleep(3.5)

for t in threads:
    t.join()
