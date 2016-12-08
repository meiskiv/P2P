import socket
import json
import thread
import quadro as q
import base64
import os

HOST = '192.168.25.27'  # Endereco IP do Servidor
PORT = 54321  # Porta que o Servidor esta
LISTAARQ_SERVIDOR = os.path.realpath('files/arquivos_server.txt')


def send_rli():
    with open(LISTAARQ_SERVIDOR,'r') as f:
        arquivos = f.read().splitlines()
        f.close()
        arquivos = q.Quadro('rli', arquivos).jsondumps()
        return arquivos


def send_rar(nome_arq):
    arq = []
    arq.append(nome_arq)
    ls = open(LISTAARQ_SERVIDOR + nome_arq, 'rb')
    arq.append(base64.encodestring(ls.read()))
    ls.close()
    arq = q.Quadro('rar', arq).jsondumps()
    print 'send_rar():', arq
    return arq

while True:
    def conectado(con, cliente):
        print '\nConectado por', cliente

        while True:
            quadro = con.recv(1024)
            deserj = json.loads(quadro)
            print cliente, quadro, '\n'

            # envia para o cliente a lista de arquivos que possui
            if (deserj['tipo']) == 'pli':
                rli = send_rli()
                print '\tquadroRLI  ', rli
                con.sendall(rli)

            # recebe do cliente a lista de arquivos para enviar
            if (deserj['tipo']) == 'par':
                print 'Requisicao do cliente: ', deserj['dados']
                arquivos = deserj['dados']
                for i in range(len(arquivos)):
                    arq = arquivos[i]
                    print arq
                    rar = send_rar(arq)
                    p = con.sendall(rar)
                    if p is None:
                        print 'rar enviado com sucesso'
                    else: print 'ar nao enviado'

                print 'Finalizando conexao do cliente', cliente
                con.close()
                thread.exit()


    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(5)

    while True:
        con, cliente = tcp.accept()
        thread.start_new_thread(conectado, tuple([con, cliente]))

    tcp.close()
