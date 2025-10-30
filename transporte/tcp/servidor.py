import socket

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
    # Aceita a conexão com cliente
    clientSocket, address = s.accept()

    print(f"Connection from {address} has been established")

    # Mensagem do cliente
    msg = clientSocket.recv(1024)
    mensagem = msg.decode("utf-8")

    if mensagem == "fechar":
        break

    # Imprime mensagem do cliente    
    print(f"Mensagem recebida: {mensagem}")
    resposta = f"Obrigado cliente {i}!"

    # Envia mensagem para o cliente
    clientSocket.send(bytes(resposta, "utf-8"))

    # Fecha a conexão com cliente
    clientSocket.close()
    i += 1

# Fecha o servidor    
s.close()