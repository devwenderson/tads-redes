import socket
import json
from myipaddress import IPAddress

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Para tornar o socket reusável
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Configurações de porta e endereço
porta = 4444
host = "0.0.0.0"
server_addr = (host, porta)
s.bind(server_addr)

# Tamaho da fila de espera
s.listen(1)

# Index do cliente (coisa para deixar mais bonitinho)
i = 1
while True:
    print("Aguardando conexão com o cliente")
    # Aceita a conexão com cliente
    clientSocket, address = s.accept()

    print(f"Connection from {address} has been established")
    # Mensagem do cliente
    received_bytes = clientSocket.recv(1024)
    option = received_bytes.decode("utf-8")
    print(f"Opção escolhida: {option}")

    if option == "/fechar":
        resposta = "\n----- Encerrando processo... -----"
        clientSocket.send(resposta.encode("utf-8"))

        resposta = "Obrigado pelo contato"
        clientSocket.send(resposta.encode("utf-8"))
        break

    while option == "1": # IP address
        resposta = "Vamos brincar com endereços IP!"
        clientSocket.send(resposta.encode("utf-8"))

        received_bytes = clientSocket.recv(4096)
        if (received_bytes):
            json_str = received_bytes.decode("utf-8")
            context = json.loads(json_str)

            endereco = context["endereco"]
            mascara = context["mascara"]

            resposta = "\n----- Tratando os dados... -----\n"
            ip = IPAddress(endereco, mascara)
            ip_str = f"{ip}"
            clientSocket.send(ip_str.encode("utf-8"))

            received_bytes = clientSocket.recv(512)

            if (received_bytes):
                option2 = received_bytes.decode("utf-8")

                if (option2 == "1"):
                    received_bytes = clientSocket.recv(4096)
                    if (received_bytes):
                        endereco = received_bytes.decode("utf-8")
                        resposta_rede = "Pertence" if ip.pertence_a_rede(endereco) else "Não pertence" 
                        clientSocket.send(resposta_rede.encode("utf-8"))
                elif (option2 == "/fechar"):
                    option = "/fechar"
                    
            
    
    resposta = "Obrigado pelo contato"
    # Envia mensagem para o cliente
    clientSocket.send(resposta.encode("utf-8"))

    # Fecha a conexão com cliente
    clientSocket.close()
    i += 1

# Fecha o servidor    
s.close()