import socket
import threading
import time

def atenderClientesSimultaneos(conexao, cliente):
    print("Conectado por",  cliente)

    # processando a mensagem
    time.sleep(5)

    mensagem = conexao.recv(1024)
    print("Cliente ", cliente[0], "; Mensagem recebida: ", mensagem)  
    conexao.close()
    print("Cliente ", cliente[0], " saiu")

host = '127.0.0.1'  # endereco IP do Servidor
porta = 5000        # porta que o servidor esta
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (host, porta)
soquete.bind(origem)
soquete.listen(0) 

while True:
    conexao, cliente = soquete.accept()

    try:
        # criando contrutor Thread com a funcao para atender clientes simultaneos e a tupla com conexao e cliente
        thread = threading.Thread(target=atenderClientesSimultaneos, args=(conexao, cliente)) # o que tiver no target usa o run
        thread.start()
    except:
        print("Erro na conexao!")