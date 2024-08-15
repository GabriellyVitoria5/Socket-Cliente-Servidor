import socket
import threading

lista_de_mensagens = []

def atenderClientesSimultaneos(conexao, cliente):
    
    # receber o nome do cliente
    nome = conexao.recv(1024).decode("utf-8")
    print "Conectado por:",  nome , cliente

    while True:
        
        # receber a escolha do cliente
        resposta_cliente_opcao = conexao.recv(1024).decode('utf-8')

        if resposta_cliente_opcao == '1':
            print nome, "escolheu a opcao 1"

        
        elif resposta_cliente_opcao == '2':
            print nome, "escolheu a opcao 2"
        
        elif resposta_cliente_opcao == '3':
            print nome, " escolheu a opcao 3"
            print "Finalizando conexao com", nome, "..."
            
            conexao.close()
            break    

host = '127.0.0.1'  # endereco IP do Servidor
porta = 5000        # porta que o servidor esta
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # definir conexao com TCP
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
