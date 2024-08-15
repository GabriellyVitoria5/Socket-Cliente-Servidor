import socket

# criar e abrir conexao
host = '127.0.0.1'     # Endereco IP do Servidor
porta = 5000           # Porta que o Servidor esta
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = (host, porta)
soquete.connect(destino)

# enviar o nome do cliente para o servidor 
nome = raw_input("Informe seu nome: ")
soquete.send(nome.encode('utf-8'))

soquete.close()