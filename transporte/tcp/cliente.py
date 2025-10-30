import socket

# Cria socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuração de porta e endereço
porta = 4444
servidor = "127.0.0.1"
client_addr = (servidor, porta) 
s.connect((servidor, porta))

# Enviar mensagem para o servidor
msg = input("Sua mensagem: ")
s.send(msg.encode("utf-8"))

# Resgatar mensagem do servidor
resposta = s.recv(1024)
print(f"Resposta: {resposta}".format(resposta.decode("utf-8")))