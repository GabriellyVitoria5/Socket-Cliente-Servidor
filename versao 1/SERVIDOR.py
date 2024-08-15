host = '127.0.0.1' # Endereco IP do Servidor
porta = 5000       # Porta que o Servidor esta
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (host, porta)
soquete.bind(origem)
soquete.listen(0)
while True:
    conexao, cliente = soquete.accept()
    print ('Conectado por', cliente)
    mensagem = conexao.recv(1024)
    print ("Cliente ", cliente[0], "Recebida: ", mensagem)
    conexao.close()