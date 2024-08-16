import socket
import threading

def escutarOutrosClientes(soquete):
     while True:
        try:
            conexao, cliente = soquete.accept()
            mensagem = conexao.recv(1024)
            print("\nMensagem recebida de", cliente, ":", mensagem.decode())
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
        print ("Enviando mensagens para todos online...")
        # listar todo mundo que mandou...

    else:
        # verificar se o destinatario e conhecido
        print ("Enviando mensagem privada...")
        destinatario = raw_input("Informe o nome do destinatario: ")
        
        

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
porta_cliente = 50001 
soquete_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (host_cliente, porta_cliente)
soquete_cliente.bind(origem)
soquete_cliente.listen(0) 

thread_escutar_clientes = threading.Thread(target=escutarOutrosClientes, args=(soquete_cliente,))
thread_escutar_clientes.daemon = True # thread sera encerrada quando o programa principal terminar
thread_escutar_clientes.start()

endereco_cliente = {} # ip de clientes que ja mandou mensagem antes
lista_mensagens_recebidas = [] # cliente vai armazenar suas proprias mensagens

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