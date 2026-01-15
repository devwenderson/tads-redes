import socket, threading, random, time, uuid

BROADCAST_PORT = 50000
BROADCAST_ADDR = "<broadcast>"
BROADCAST_DELAY = 5

class Cliente:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_port = random.randint(20000, 40000)
        self.running = True
        self.mac = self.get_local_mac()

    def get_local_mac(self):
        mac_int = uuid.getnode()
        return ":".join(f"{(mac_int >> 8*i) & 0xff:02x}" for i in reversed(range(6)))
    

    # ----------------------------------------------------
    # UDP: broadcast de descoberta
    # ----------------------------------------------------
    def send_broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        while self.running:
            mensagem = f"DISCOVER_REQUEST;PORT={self.tcp_port}"
            sock.sendto(mensagem.encode(), (BROADCAST_ADDR, BROADCAST_PORT))
            print(f"[Broadcast enviado] {mensagem}")
            time.sleep(BROADCAST_DELAY)

    # ----------------------------------------------------
    # TCP: servidor interno para responder comandos
    # ----------------------------------------------------
    def tcp_server_receive_command(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", self.tcp_port))
        sock.listen(5)

        print(f"[Cliente] Servidor TCP escutando na porta {self.tcp_port}...")

        while self.running:
            conn, addr = sock.accept() # SYN+ACK 
            
            print(f"[TCP] Conexão recebida de {addr}")
            data = conn.recv(1024).decode()
            
            if data == "GET_MAC":
                response = f"MAC_ADDRESS;{self.mac}"
                conn.send(response.encode())
                print(f"[MAC enviado via TCP] {self.mac}")
            
            conn.close() # FIN

    # ----------------------------------------------------
    # UDP: Troca de dados com o servidor
    # ----------------------------------------------------
    def send_to_server(self, mensagem, endereco):
        """
            Entradas:
                mensagem: string
                endereco: (str, int) - ("123.93.29.12", 123456)
        """
        mensagem_bytes = mensagem.encode()
        self.sock.sendto(mensagem_bytes, endereco)

    def recover_from_server(self):
        """
            Saídas: (bytes, address)
        """
        mensagem_recebida = self.sock.recvfrom(2048)
        return mensagem_recebida
    
    def main_logic(self):
        while self.running:
            time.sleep(5)
    
    def start(self):
        print(f"[Cliente] TCP_PORT={self.tcp_port} | MAC={self.mac}")

        threading.Thread(target=self.send_broadcast, daemon=True).start()
        threading.Thread(target=self.tcp_server_receive_command, daemon=True).start()

        self.main_logic()

if __name__ == "__main__":
    cliente = Cliente()
    cliente.start()

# HOST = "10.220.0.42"
# PORT = 12000
# cliente = Cliente()

# while True:
#     print("Digite (Sair) para sair")
#     mensagem_envio = input("Digite uma mensagem: ")

#     if mensagem_envio == "sair":
#         break

#     cliente.send_to_server(mensagem_envio, (HOST, PORT))
#     resposta, endereco = cliente.recover_from_server()
#     print(f"Resposta: {resposta.decode()} - Endereço: {endereco}")

# print("Saiu")
