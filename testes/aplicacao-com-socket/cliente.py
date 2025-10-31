"""
encode() - Só funciona com strings
bytes() - Usa em dados não-strings
"""

import socket
import json
# Cria socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuração de porta e endereço
porta = 4444
servidor = "127.0.0.1"
client_addr = (servidor, porta) 
s.connect((servidor, porta))

# Enviar mensagem para o servidor
def menu():
    print("1 - Endereços IP\n")
    print("Digite '/fechar' para encerrar\n")
    return input("Selecione uma opção: ")
option = menu()
s.send(option.encode("utf-8"))

while option == "1":
    # Resgatar mensagem do servidor
    received_bytes = s.recv(1024)
    resposta = received_bytes.decode("utf-8")
    print(f"O servidor diz: {resposta}")
    endereco = input("Informe o endereço IP: ")
    mascara = input("Informe a máscara: ")
    
    context = {
        "endereco": endereco,
        "mascara": mascara
    }

    json_str = json.dumps(context)
    s.send(json_str.encode("utf-8"))
    
    print("\n----- Aguardando mensagem do servidor... -----\n")

    received_bytes = s.recv(2048)
    ip_str = received_bytes.decode("utf-8")
    print(f"Rede: {ip_str}")

    print("\n----- Que outra operação você quer fazer? -----\n")
    print(f"1 - Verificar se um endereço está dentro do alcance de {ip_str}")
    
    option2 = input("Informe a opção: ")
    s.send(option2.encode("utf-8"))

    if (option2 == "1"):
        endereco = input("Informe o endereço para comparar: ")
        s.send(endereco.encode("utf-8"))        
        print("\n----- Aguardando mensagem do servidor... -----\n")
        received_bytes = s.recv(4096)
        resposta_rede = received_bytes.decode("utf-8")
        print(f"{endereco} {resposta_rede} ao alcande de {ip_str}")

    option = menu()
    s.send(option.encode("utf-8"))

if option == "/fechar":
    received_bytes = s.recv(2048)
    resposta = received_bytes.decode("utf-8")
    print(resposta) 

    received_bytes = s.recv(2048)
    resposta = received_bytes.decode("utf-8")
    print(resposta) 