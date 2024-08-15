import socket

# criar e abrir conexao
host = '127.0.0.1'     # Endereco IP do Servidor
porta = 5000           # Porta que o Servidor esta
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
destino = (host, porta)
soquete.connect(destino)

endereco_cliente = {} # ip, porta e status do cliente que ja mandou mensagem antes
lista_mensagens_recebidas = [] # cliente vai armazenar suas proprias mensagens

# enviar o nome do cliente para o servidor 
nome = raw_input("Informe seu nome: ")
soquete.send(nome.encode('utf-8'))

# loop do menu de opcoes
while True:
        
    menu = "\n................. Menu .................\n\nEscolha uma das opcoes\n1. Enviar mensagem para outro cliente\n2. Listar mensages recebidas\n3. Listar IP de clientes conhecidos\n4.cListar clientes conectados\n5. Sair"
    print(menu)

    # ler a opcao escolhida e enviar ao servidor
    resposta_opcao = raw_input("\nOpcao escolhida: ")
    soquete.send(resposta_opcao.encode('utf-8'))
    
    if resposta_opcao == '1':
        print("\n........... Enviar mensagens para um cliente ...........\n")
        

    elif resposta_opcao == '2':
        print("\n............. Listar mensagens recebidas .............\n")



    elif resposta_opcao == '3':
        print("\n........... Listar IP de clientes conhecidos ...........\n")


    elif resposta_opcao == '4':
        print("\n............. Listar clientes conectados .............\n")



    elif resposta_opcao == '5':
        print("\n................. Sair .................\n")
        print("Encerrando a conexao com o servidor")
        break
        
    else:
        print("Opcao invalida")

soquete.close()