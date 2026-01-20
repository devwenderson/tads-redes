import socket, threading, random, time, uuid, psutil

BROADCAST_PORT = 50000
BROADCAST_ADDR = "<broadcast>"
BROADCAST_DELAY = 5

class Cliente:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_port = random.randint(20000, 40000)
        # self.tcp_port = 22222
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
    # TCP: servidor interno para responder comandos do servidor
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

            if data == "GET_RESOURCES":
                # USO DA CPU EM PORCENTAGEM
                qtd_core = psutil.cpu_count(logical=False)
                cpu_usage = psutil.cpu_percent(interval=2)
                free_ram = (psutil.virtual_memory().available)//(1024)**3
                free_disk = (psutil.disk_usage("C:\\").free)//(1024)**3
                os_name = ""
                if (psutil.WINDOWS): os_name = "Windows"
                elif (psutil.LINUX): os_name = "Linux"
                elif (psutil.MACOS): os_name = "Mac OS"

                response = (
                    "RESOURCES;"
                    f"os_name={os_name};"
                    f"qty_core={qtd_core};"
                    f"cpu_usage={cpu_usage};"
                    f"free_ram={free_ram};"
                    f"free_disk={free_disk}"
                )


                conn.send(response.encode())

            
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
