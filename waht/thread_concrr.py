import socket
import json
import thread

HOST = '192.168.25.27'              # Endereco IP do Servidor
PORT = 54321                        #  Porta que o Servidor esta


#json_dados = '{"tipo": tipo, "dados": dados'}'
def send_rar(dados):
    with open ('/home/meiski/PycharmProjects/P2P/pcp/files/arquivos.txt') as f:
        arqs = f.readline()
        if arqs == dados:
            #lógica pra mandar nome do arquivo e arquivo codificado blah blah


while True:
    def conectado(con, cliente):
        print 'Conectado por', cliente

        while True:
            quadro = con.recv(j)
            deserj = json.loads(quadro)
            print deserj
            print cliente, quadro

            if (deserj['tipo']) == 'par':
                send_rar(quadro.dados)
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


