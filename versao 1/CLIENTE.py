import socket
import time
host = '127.0.0.1'     # Endereco IP do Servidor
porta = 5000           # Porta que o Servidor esta
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = (host, porta)
soquete.connect(destino)
soquete.send("ola mundo")

print("Aguardando para fechar conexao...")
time.sleep(5)
print("Fim da conexao")

soquete.close()