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
            print"Aguardando", nome, "enviar as informacoes para o envio da mensagem..."

            # cliente informou o destinatario e a mensagem que sera envaiada a ele
            destinatario = conexao.recv(1024).decode('utf-8')
            mensagem = conexao.recv(1024).decode('utf-8')
            
            # tupla com 3 argumentos
            lista_de_mensagens.append((destinatario, nome, mensagem))

            print "Mensagem armazenada, esperando", destinatario, "solicitar suas mensagens"
            conexao.send("Mensagem enviada".encode('utf-8'))
        
        elif resposta_cliente_opcao == '2':
            print nome, "escolheu a opcao 1"
            print "Enviando mensagens enviadas para", nome
            
            # criando uma lista com as mensagens enviadas para o cliente atual 
            mensagens_destinatario = list(filter(lambda nome_destinatario: nome_destinatario[0] == nome, lista_de_mensagens))
           
            if len(mensagens_destinatario) != 0:

                # ordenar a lista pelo nome do destinatario (argumento 1)
                mensagens_destinatario.sort()
                
                # extraindo dados da tupla para formar a mensagem
                mensagens = []
                for mensagem in mensagens_destinatario:
                    mensagem_string = (mensagem[1] + ": " + mensagem[2])
                    mensagens.append(mensagem_string)
                
                # juntar as mensagens em uma string
                mensagens_quebra_linha = "\n".join(mensagens)

                conexao.send(mensagens_quebra_linha)
            else:
                conexao.send("Voce nao tem mensagens recebidas".encode('utf-8'))
        
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
