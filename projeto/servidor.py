import os
import socket, threading, time, psutil

BROADCAST_PORT = 50000

class ClienteInfo:
    def __init__(self, ip, tcp_port):
        self.ip = ip
        self.tcp_port = tcp_port
        self.last_seen = time.time()
        self.last_msg = ""
        self.mac = None
    
    def update(self, msg):
        self.last_msg = msg
        self.last_seen = time.time()
    
    def __repr__(self):
        age = round(time.time() - self.last_seen, 1)
        return (f"{self.ip}:{self.tcp_port} | MAC={self.mac} | "
                f"Ultima mensagem='{self.last_msg}' | {age}s atrás")


class Servidor:
    def __init__(self):
        self.clientes = {} # chave: (ip, tcp_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", BROADCAST_PORT))

    # -----------------------------------------------
    # ESCUTA BROADCASTS
    # -----------------------------------------------
    def listen_broadcast(self):
        # print(f"[Servidor] Ouvindo broadcasts na porta {BROADCAST_PORT}")

        while True:
            data, addr = self.sock.recvfrom(1024)
            mensagem = data.decode()
            ip = addr[0]

            # print(f"[Broadcast de {ip}] {mensagem}")

            if mensagem.startswith("DISCOVER_REQUEST"):
                tcp_port = mensagem.split("=")[1]
                key = (ip, int(tcp_port))

                # Salva cliente com chave composta (ip, tcp_port)
                if key not in self.clientes:
                    self.clientes[key] = ClienteInfo(ip, tcp_port)
                    print(f"[Novo cliente] {ip}:{tcp_port}")
            
            # Atualiza "last_msg" e "last_seen"
            self.clientes[key].update(mensagem)

            # Envia resposta UDP
            self.sock.sendto("DISCOVER_RESPONSE".encode(), addr)

    def send_request_to_client(self, command, key):
        """
        key: (ip_address, tcp_port)
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(key) # SYN

        sock.send(command.encode())
        response = sock.recv(1024).decode()
        sock.close()
        return response


    # -----------------------------------------------
    # SOLICITA MAC VIA TCP
    # -----------------------------------------------
    def ask_me_tcp(self, key):
        """
        key: (ip_address, tcp_port)
        """

        if key not in self.clientes:
            print("[Erro] Cliente não encontrado")
            return
        
        ip_address, tcp_port = key
        print(f"[Servidor] Tentando conexão com o cliente {ip_address}:{tcp_port} via TCP\n")

        try:
            response = self.send_request_to_client("GET_MAC", (ip_address, tcp_port))

            if response.startswith("MAC_ADDRESS"):
                mac = response.split(";")[1]
                self.clientes[key].mac = mac
                print(f"[MAC recebido via TCP] {ip_address}:{tcp_port} => {mac}\n")

        except Exception as e:
            print(f"[Erro] Erro de conexão via TCP: {e}\n")
    
    # ---------------------------------------------------------
    # SOLICITA DADOS DE RECURSOS DO COMPUTADOR CLIENTE VIA TCP
    # ---------------------------------------------------------
    def ask_me_resources(self, key):
        """
        key: (ip_address, tcp_port)
        """
        
        if key not in self.clientes:
            print("[Erro] Cliente não encontrado\n")
            return

        ip_address, tcp_port = key
        print(f"[Servidor] Tentando conexão com o cliente {ip_address}:{tcp_port} via TCP\n")

        try:
            response = self.send_request_to_client("GET_RESOURCES", (ip_address, tcp_port))
            if (response.startswith("RESOURCES")):
                resources = response.split(";")[1]
                return resources
        
        except Exception as e:
            print(f"[Erro] Erro de conexão TCP: {e}\n")

    def list_clients(self):
        for ip_address, tcp_port in self.clientes:
            print(f"{ip_address}:{tcp_port} -> {self.clientes[(ip_address, tcp_port)]}")
    
    def menu(self):
        while True:
            print("\n=== MENU SERVIDOR ===")
            opcoes = "1 - Listar clientes\n"
            opcoes += "2 - Solicitar MAC de um cliente via TCP\n" 
            opcoes += "3 - Solicitar MAC de todos os clientes via TCP\n" 
            opcoes += "4 - Solicitar dados dos recursos de um cliente via TCP\n" 
            opcoes += "0 - Sair\n"
            print(opcoes)
            op = input("> ")

            match op:
                case "1":
                    os.system("cls")
                    print("\n--- Clientes ---")

                    self.list_clients()

                case "2":
                    os.system("cls")
                    self.list_clients()
                    ip_address = input("Digite o IP: ")
                    tcp_port = int(input("Digite a porta TCP do cliente: "))
                    self.ask_me_tcp((ip_address, tcp_port))

                case "3":
                    for key in self.clientes:
                        self.ask_me_tcp(key)

                case "4":
                    os.system("cls")
                    self.list_clients()
                    ip_address = input("Digite o IP: ")
                    tcp_port = int(input("Digite a porta TCP do cliente: "))
                    resources = self.ask_me_resources((ip_address, tcp_port))
                    print(f"Recursos do cliente {ip_address}:{tcp_port} ->\n{resources}")

                case "0":
                    exit()

                case _:
                    print("[Erro] Opção inválida")

    def start(self):
        threading.Thread(target=self.listen_broadcast, daemon=True).start()
        self.menu()
                
if __name__ == "__main__":
    Servidor().start()


# class Servidor:
#     def __init__(self):
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#     def bind_server(self, host, port):
#         self.sock.bind((host, port))

#     def send_to_client(self, mensagem, endereco):
#         """
#             Entradas:
#                 mensagem: string
#                 endereco: (str, int) - ("123.93.29.12", 123456)
#         """
#         mensagem_bytes = mensagem.encode()
#         self.sock.sendto(mensagem_bytes, endereco)

#     def recover_from_client(self):
#         """
#             Saída: (bytes, address)
#         """
#         mensagem_recebida = self.sock.recvfrom(2048)
#         return mensagem_recebida



# HOST = ""
# PORT = 12000

# servidor = Servidor()
# servidor.bind_server(HOST, PORT)

# while True:
#     print("<<< ESCUTANDO... >>>")
#     mensagem_recebida, endereco = servidor.recover_from_client()
#     print(f"Dados | Endereço: {endereco} - Mensagem: {mensagem_recebida}")
#     mensagem_envio = mensagem_recebida.decode().lower()
#     servidor.send_to_client(mensagem_envio, endereco)
    



