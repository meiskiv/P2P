import socket
import json
import thread
import quadro

HOST = '10.0.2.15'              # Endereco IP do Servidor
PORT = 54321                        #  Porta que o Servidor esta


#json_dados = '{"tipo": tipo, "dados": dados'}'
def send_rli():
    with open('/home/user/PycharmProjects/P2P/pcp/files/arquivos.txt') as f:
        arquivos = f.readlines()
        print arquivos
        f.close()
    quadro.Quadro


            #logica pra mandar nome do arquivo e arquivo codificado blah blah


while True:
    def conectado(con, cliente):
        print 'Conectado por', cliente

        while True:
            quadro = con.recv(1024)
            deserj = json.loads(quadro)
          #  print deserj
            print cliente, quadro

            if (deserj['tipo']) == 'pli':
                 send_rli()
            print 'Finalizando conexao do cliente', cliente
            con.close()
            thread.exit()

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)

    while True:
        con, cliente = tcp.accept()
        thread.start_new_thread(conectado, tuple([con, cliente]))

    tcp.close()


