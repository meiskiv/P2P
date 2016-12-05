import socket
import server_thread

#servidor vou ter que passar por parametro
HOST = '192.168.1.6'              # Endereco IP do Servidor
PORT = 54321            # Porta que o Servidor esta

def conectado(con, cliente):
    print 'Conectado por', cliente

    while True:
        msg = con.recv(1024)
        if not msg: break
        print cliente, msg

    print 'Finalizando conexao do cliente', cliente
    con.close()
    server_thread.exit()

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    server_thread.start_new_thread(conectado, tuple([con, cliente]))

tcp.close()