import socket
import threading
import json

# o nome vai ser a chave para diferenciar clientes
lista_clientes = {}

def atenderClientesSimultaneos(conexao, cliente):
    
    # receber o nome do cliente 
    nome = conexao.recv(1024).decode("utf-8")
    ip_cliente = conexao.recv(1024).decode("utf-8")
    porta_cliente = int(conexao.recv(1024).decode("utf-8"))
    
    print "Conectado por:",  nome , cliente

    # atualizar ou criar o cliente no dicionario
    lista_clientes[nome] = {"endereco_cliente": (ip_cliente, porta_cliente),"endereco_servidor": cliente, "status": "online"}

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
            
                # filtrar apenas os clientes online
                clientes_online = {}
                for nome, dados in lista_clientes.items():
                    if dados["status"] == "online":
                        clientes_online[nome] = dados

                # enviar json com apenas com os clientes online para o cliente            
                clientes_online_json = json.dumps(clientes_online)
                conexao.send(clientes_online_json.encode('utf-8'))

            else:
                print nome, "vai enviar mensagem privada para um cliente"

                # caso 1: cliente conhece outro cliente, o servidor nao precisa fazer nada
                # caso 2: cliente nao tem ip do destinatario

                cliente_conhece_destinatario = conexao.recv(1024).decode('utf-8')

                if cliente_conhece_destinatario == "c":
                    print nome, "ja conhece o ip do destinatario"
                else:
                    print nome, "precisa de um ip"
                    destinatario = conexao.recv(1024).decode('utf-8')
                    print "Procurar ip de:", destinatario

                    if destinatario in lista_clientes and lista_clientes[destinatario]["status"] == "online":
                        dados_destinatario = json.dumps(lista_clientes[destinatario])
                        conexao.send(dados_destinatario.encode('utf-8'))
                    else:
                        # mandar json vazio se o servidor nao conhece o destinatario
                        conexao.send(json.dumps({}).encode('utf-8'))

        
        elif resposta_cliente_opcao == '2':
            print nome, "escolheu a opcao 2"
            # servidor nao precisa entregar nada para o cliente nessa opcao

        elif resposta_cliente_opcao == '3':
            print nome, "escolheu a opcao 3"

            # enviar lista para o cliente fazer a varificacao
            status_clientes = json.dumps(lista_clientes)
            conexao.send(status_clientes.encode('utf-8'))

        elif resposta_cliente_opcao == '4':
            print nome, "escolheu a opcao 4"

            # verificar opcao 4 quando nao tem clientes online no servidor.....
            
            # filtrar apenas os clientes online
            clientes_online = {}
            for nome, dados in lista_clientes.items():
                if dados["status"] == "online":
                    clientes_online[nome] = dados

            # enviar json com apenas com os clientes online para o cliente            
            clientes_online_json = json.dumps(clientes_online)
            conexao.send(clientes_online_json.encode('utf-8'))

            print("Dados sobre os clientes online enviados")
           
        elif resposta_cliente_opcao == '5':
            print nome, " escolheu a opcao 5"
            print "Finalizando conexao com", nome, "..."

            # atualizar status do cliente
            lista_clientes[nome] = {"endereco_cliente": (ip_cliente, porta_cliente), "endereco_servidor": cliente, "status": "offline"}

            print(lista_clientes[nome])
            print(lista_clientes)

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
