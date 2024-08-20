import socket
import threading
import time
import random
import json

def escutarOutrosClientes(soquete):
     while True:
        try:
            time.sleep(3) # tempo para o print nao sobrepor a interacao com o menu da thread de conexao com o servidor
            conexao, cliente = soquete.accept()
            mensagem = conexao.recv(1024)
            lista_mensagens_recebidas.append(mensagem)
            print "\n", cliente, "te enviou uma mensagem" 
            conexao.close()
        except Exception as e:
            print("Erro ao receber mensagem:", e)
            continue
        
# opcao 1
def enviarMensagens():
    print("\n........... Enviar mensagens para um cliente ...........\n")

    # por padrao vai enviar mensagens para todos online 
    escolha_envio = raw_input("Enviar mensagem privada para um usuario? (s/n): ")
    soquete_servidor.send(escolha_envio.encode('utf-8'))

    if escolha_envio == "n":
        print ("\nEnviando mensagens para todos online...")
        time.sleep(3)

        # pedir ao servidor informacoes de todos os clientes online
        servior_clientes_online_json = soquete_servidor.recv(1024).decode('utf-8')
        servior_clientes_online = json.loads(servior_clientes_online_json)
        
        if len(servior_clientes_online) > 1:

            mensagem = raw_input("Digite sua mensagem: ")
            mensagem_com_nome = nome + ": " + mensagem

            for cliente_online, dados in servior_clientes_online.items():
                if cliente_online != nome:
                    ip_c, porta_c = dados["endereco_cliente"]
                    ip_s, porta_s = dados["endereco_cliente"]
                    soquete_enviar_mensagem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    endereco_destinatario = (ip_c, porta_c)
                    endereco_destinatario_servidor = (ip_s, porta_s)
                    status = dados["status"]
                    
                    soquete_enviar_mensagem.connect(endereco_destinatario)
                    soquete_enviar_mensagem.send(mensagem_com_nome.encode('utf-8'))

                    #atualizar lista de clientes conhecidos
                    endereco_cliente[cliente_online] = {"endereco_cliente": endereco_destinatario, "endereco_servidor": endereco_destinatario_servidor,"status": status}

            print("\nMensagens enviadas para todos online.")
        
        else:
            print("\nNenhum cliente online")

    else:
        # verificar se o destinatario e conhecido
        print ("Enviando mensagem privada...")
        destinatario = raw_input("\nInforme o nome do destinatario: ")
        
        if destinatario in endereco_cliente:

            # indicar ao servidor que o cliente e conhecido: 'c'
            soquete_servidor.send("c".encode('utf-8'))
            time.sleep(1)

            soquete_servidor.send(destinatario.encode('utf-8'))
            time.sleep(1)

            # receber do servidor status do destinatario
            servidor_status_destinatario = soquete_servidor.recv(1024).decode('utf-8')

            if servidor_status_destinatario == "online":

                # enviar mensagem deireto para o cliente
                mensagem = raw_input("Digite sua mensagem: ")
                mensagem_com_nome = nome + ": " + mensagem # se deixar a virgula na hora de enviar entende como uma tupla
                
                # montando o socket
                soquete_enviar_mensagem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip_destinatario, porta_destinatario = endereco_cliente[destinatario]["endereco_cliente"]
                
                endereco_destinatario = (porta_destinatario, ip_destinatario)
                print(endereco_destinatario)
                
                soquete_enviar_mensagem.connect(endereco_destinatario)
                soquete_enviar_mensagem.send(mensagem_com_nome.encode('utf-8'))
                
                print("\nMensagem enviada")

            else:
                print("\nCliente nao esta online, nao foi possivel enviar mensagem")

        else:
            # pedir ao servidor o endereco do destinatario
            print("Cliente nao encontrado, solicitando IP ao servidor...")

            # indicar ao servidor que o cliente e conhecido: 'd'
            soquete_servidor.send("d".encode('utf-8'))
            time.sleep(1)
            soquete_servidor.send(destinatario.encode('utf-8'))
            time.sleep(1)

            servidor_dados_destinatario_json = soquete_servidor.recv(1024).decode('utf-8')
            dados_destinatario = json.loads(servidor_dados_destinatario_json)
            
            if dados_destinatario:
                mensagem = raw_input("Digite sua mensagem: ")
                mensagem_com_nome = nome + ": " + mensagem

                # atualizando lista de clientes conhecidos
                endereco_cliente[destinatario] = dados_destinatario

                soquete_enviar_mensagem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                ip, porta = dados_destinatario["endereco_cliente"]
                endereco_destinatario = (ip, porta)
                print(endereco_destinatario)

                soquete_enviar_mensagem.connect(endereco_destinatario)
                soquete_enviar_mensagem.send(mensagem_com_nome.encode('utf-8'))
                
                print("\nMensagem enviada")
            else:
                print("\nDestinatario nao encontrado no servidor.")
        

# opcao 2
def listarMensagensRecebidas():
    print("\n............. Listar mensagens recebidas .............\n")
    
    if len(lista_mensagens_recebidas) == 0:
        print("Voce nao tem mensagens")
    for mensagens in lista_mensagens_recebidas:
        print(mensagens)

# opcao 3
def listarIPsConhecidos():
    print("\n........... Listar IP de clientes conhecidos ...........\n")
    print("Nome | Endereco IP | Porta | Status")

    time.sleep(2)

    # atualizar o status dos clientes conhecidos, se estao online ou nao, antes de exibir

    # cliente recebe json do servidor e converte de volta em dicionario
    servidor_status_cliente_json = soquete_servidor.recv(1024).decode('utf-8')
    servidor_status_cliente = json.loads(servidor_status_cliente_json)

    # atualizar status
    for cliente, dados in endereco_cliente.items():
        if cliente in servidor_status_cliente:
            if dados["status"] != servidor_status_cliente[cliente]["status"]:
                dados["status"] = servidor_status_cliente[cliente]["status"]

    for cliente, dados in endereco_cliente.items():
        ip, porta = dados["endereco_cliente"]
        status = dados["status"]
        print cliente, "|", ip,"|", porta, "|", status

    #print(endereco_cliente)

# opcao 4
def listarClientesOnline():
    print("\n............. Listar clientes conectados .............\n")
    print("Solicitando ao servidor todos os clientes conectados agora...")

    time.sleep(2)

    # verificar opcao 4 quando nao tem clientes online no servidor.....

    # receber os dados dos cliente online em json e transformar em dicionario
    servidor_resposta_clientes_online_json = soquete_servidor.recv(1024).decode('utf-8')
    servior_clientes_online = json.loads(servidor_resposta_clientes_online_json)
    #print(servior_clientes_online)

    cont = 0
    # imprimir dados e atualizar lista de clientes conhecidos
    print("\nNome | Endereco IP | Porta")
    for cliente, dados in servior_clientes_online.items():
        porta_c, ip_c = dados["endereco_cliente"]
        ip_s, porta_s = dados["endereco_servidor"]
        status = dados["status"]
        print cliente, ",", ip_c, ",", porta_c

        if cliente not in endereco_cliente:
            cont += 1
        
        # atualizar lista de clientes conhecidos se houver clientes novos
        endereco_cliente[cliente] = {"endereco_cliente": (ip_c, porta_c), "endereco_servidor": (ip_s, porta_s),"status": status}
        
    if cont > 0:
        print("\nLista de clientes conhecidos atualizada")

# opcao 5
def desconectarDoServidor():
    print("\n................. Sair .................\n")
    print("Encerrando a conexao com o servidor")
    soquete_servidor.close()

# criar e abrir conexao com servidor
host_servidor = '127.0.0.1'     
porta_servidor = 5000  
soquete_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino_servidor = (host_servidor, porta_servidor)
soquete_servidor.connect(destino_servidor)

# criar e abrir conexao com outro clientes
host_cliente = '127.0.0.1'  
porta_cliente = random.randint(5002, 6000) # sortear porta para clientes simultaneaos se conectarem entre si
soquete_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (host_cliente, porta_cliente)
soquete_cliente.bind(origem)
soquete_cliente.listen(0) 

thread_escutar_clientes = threading.Thread(target=escutarOutrosClientes, args=(soquete_cliente,))
thread_escutar_clientes.daemon = True # thread sera encerrada quando o programa principal terminar
thread_escutar_clientes.start()

endereco_cliente = {} # nome e a chave, endereco_cliente, endereco_servidor, status
lista_mensagens_recebidas = [] # cliente vai armazenar suas proprias mensagens

# enviar o nome e informacoes de conexao do cliente para o servidor 
nome = raw_input("Informe seu nome: ")
print(nome, porta_cliente)

soquete_servidor.send(nome.encode('utf-8'))
time.sleep(1)
soquete_servidor.send(host_cliente.encode('utf-8'))
time.sleep(1)
soquete_servidor.send(str(porta_cliente).encode('utf-8'))

endereco_cliente[nome] = {"endereco_cliente": (host_cliente, porta_cliente),"endereco_servidor": (host_servidor, porta_servidor), "status": "online"}

# loop do menu de opcoes
while True:
    
    # interacao entre cliente e servidor    
    menu = "\n................. Menu .................\n\nEscolha uma das opcoes\n1. Enviar mensagem para outro cliente\n2. Listar mensages recebidas\n3. Listar IP de clientes conhecidos\n4. Listar clientes conectados\n5. Sair"
    print(menu)

    # ler a opcao escolhida e enviar ao servidor
    resposta_opcao = raw_input("\nOpcao escolhida: ")
    soquete_servidor.send(resposta_opcao.encode('utf-8'))
    
    if resposta_opcao == '1':
        enviarMensagens()

    elif resposta_opcao == '2':
        listarMensagensRecebidas()

    elif resposta_opcao == '3':
        listarIPsConhecidos()

    elif resposta_opcao == '4':
        listarClientesOnline()

    elif resposta_opcao == '5':
        desconectarDoServidor()
        break
        
    else:
        print("Opcao invalida")

soquete_cliente.close()