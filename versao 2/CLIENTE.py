import socket
import threading
import time

def escutarOutrosClientes(soquete):
     while True:
        try:
            time.sleep(3) # tempo para o print nao sobrepor o interacao com o menu da thread de conexao com o servidor
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
        # pedir ao servidor ip e nome de todos os clientes online....

    else:
        # verificar se o destinatario e conhecido
        print ("Enviando mensagem privada...")
        destinatario = raw_input("\nInforme o nome do destinatario: ")
        
        if destinatario in endereco_cliente:

            # indicar ao servidor que o cliente e conhecido: 'c'
            soquete_servidor.send("c".encode('utf-8'))

            # enviar mensagem deireto para o cliente
            mensagem = raw_input("Digite sua mensagem: ")
            mensagem_com_nome = nome + ": " + mensagem # se deixar a virgula na hora de enviar entende como uma tupla
            
            soquete_enviar_mensagem = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            destino = (host_cliente, porta_cliente)
            soquete_enviar_mensagem.connect(destino)
            soquete_enviar_mensagem.send(mensagem_com_nome.encode('utf-8'))
            
            print("\nMensagem enviada")

        else:
            # pedir ao servidor o endereco do destinatario
            print("Cliente nao encontrado, solicitando IP ao servidor...")

            # indicar ao servidor que o cliente e conhecido: 'd'
            soquete_servidor.send("d".encode('utf-8'))
            soquete_servidor.send(destinatario.encode('utf-8'))
            
            time.sleep(10)
        

# opcao 2
def listarMensagensRecebidas():
    print("\n............. Listar mensagens recebidas .............\n")

# opcao 3
def listarIPsConhecidos():
    print("\n........... Listar IP de clientes conhecidos ...........\n")

# opcao 4
def listarClientesOnline():
    print("\n............. Listar clientes conectados .............\n")

# opcao 5
def desconectarDoServidor():
    print("\n................. Sair .................\n")
    print("Encerrando a conexao com o servidor")
    soquete_servidor.close()

# criar e abrir conexao com servidor
host_servidor = '127.0.0.1'     
porta_servidor = 5000  # porta que o Servidor esta
soquete_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino_servidor = (host_servidor, porta_servidor)
soquete_servidor.connect(destino_servidor)

# criar e abrir conexao com outro clientes
host_cliente = '127.0.0.1'  
porta_cliente = 5001 # erro na porta se mais clientes se conectarem, olhar depois!!!!!!!
soquete_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (host_cliente, porta_cliente)
soquete_cliente.bind(origem)
soquete_cliente.listen(0) 

thread_escutar_clientes = threading.Thread(target=escutarOutrosClientes, args=(soquete_cliente,))
thread_escutar_clientes.daemon = True # thread sera encerrada quando o programa principal terminar
thread_escutar_clientes.start()

endereco_cliente = {} # ip de clientes que ja mandou mensagem antes
lista_mensagens_recebidas = [] # cliente vai armazenar suas proprias mensagens

# inserir valor de teste no dicionario
endereco_cliente["joao"] = {"endereco": ('127.0.0.1', 5001), "status": "online"}

# enviar o nome do cliente para o servidor 
nome = raw_input("Informe seu nome: ")
soquete_servidor.send(nome.encode('utf-8'))

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