import socket
import json
import thread
import quadro as q

HOST = '192.168.25.27'              # Endereco IP do Servidor
PORT = 54321                        #  Porta que o Servidor esta


def send_rli():
    with open('/home/meiski/PycharmProjects/P2P/pcp/files/arquivos_server.txt') as f:
        arquivos = f.read().splitlines()
        f.close()
        arquivos = q.Quadro('rli',arquivos).jsondumps()
        return arquivos


def send_rar():
    print 'rar'
            #logica pra mandar nome do arquivo e arquivo codificado blah blah


while True:
    def conectado(con, cliente):
        print 'Conectado por', cliente

        while True:
            quadro = con.recv(1024)
            deserj = json.loads(quadro)
            print cliente, quadro,'\n'

            # envia para o cliente a lista de arquivos que possui
            if (deserj['tipo']) == 'pli':
                quadrorli = send_rli()
                print '\tquadroRLI  ', quadrorli
                con.sendall(quadrorli)


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


