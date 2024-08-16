import socket
import threading

# o nome vai ser a chave para diferenciar clientes
lista_clientes_online = {}

def atenderClientesSimultaneos(conexao, cliente):
    
    # receber o nome do cliente 
    nome = conexao.recv(1024).decode("utf-8")
    print "Conectado por:",  nome , cliente

    # atualizar ou criar o cliente no dicionario
    lista_clientes_online[nome] = cliente, "online"

    while True:
        
        # receber qual opcao do menu foi escolhida
        resposta_cliente_opcao = conexao.recv(1024).decode('utf-8')

        if resposta_cliente_opcao == '1':
            print nome, "escolheu a opcao 1"
            
            # receber o tipo de envio, privado ou para todos online
            resposta_cliente_envio = conexao.recv(1024).decode('utf-8')

            if resposta_cliente_envio == "n":
                # entregar a lista de todos os clientes que estao conectados
                print nome, "vai enviar mensagens para todos online"
            
                # ...

            else:
                print nome, "vai enviar mensagem privada para um cliente"

                # caso 1: cliente conhece outro cliente, o servidor nao precisa fazer nada
                # caso 2: cliente nao tem ip do destinatario

                cliente_conhece_destinatario = conexao.recv(1024).decode('utf-8')

                if cliente_conhece_destinatario == "c":
                    print(nome, "ja conhece o ip do destinatario")
                else:
                    print nome, "precisa de um ip"
                    destinatario = conexao.recv(1024).decode('utf-8')
                    print "Destinatario recebido pelo servidor:", destinatario 

        
        elif resposta_cliente_opcao == '2':
            print nome, "escolheu a opcao 2"


        elif resposta_cliente_opcao == '3':
            print nome, "escolheu a opcao 3"


        elif resposta_cliente_opcao == '4':
            print nome, "escolheu a opcao 4"

            
            
        elif resposta_cliente_opcao == '5':
            print nome, " escolheu a opcao 5"
            print "Finalizando conexao com", nome, "..."

            lista_clientes_online[nome] = cliente, 'offline'
            print(lista_clientes_online[nome])
            print(lista_clientes_online)
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
