import os
import socket, threading, time, psutil

BROADCAST_PORT = 50000
BROADCAST_DELAY = 30
VERIFY_CLIENT = 10

class ClienteInfo:
    def __init__(self, ip, tcp_port):
        self.ip = ip
        self.tcp_port = tcp_port
        self.last_seen = time.time()
        self.last_msg = ""
        self.mac = None
        self.is_online = True
        self.qty_core =  None
        self.cpu_usage = None
        self.free_ram = None
        self.free_disk = None
        self.os_name = None
    
    def updateResources(self, resoucers_dict):
        self.qty_core =  resoucers_dict["qty_core"]
        self.cpu_usage = resoucers_dict["cpu_usage"]
        self.free_ram = resoucers_dict["free_ram"]
        self.free_disk = resoucers_dict["free_disk"]
        self.os_name = resoucers_dict["os_name"]

    def update(self, msg):
        self.last_msg = msg
        self.last_seen = time.time()

    # TEMPO QUE PASSOU DESDE A ÚLTIMA MENSAGEM
    def getAge(self):
        return round(time.time() - self.last_seen, 1)
    
    def getIsOnline(self):
        return self.is_online
    
    def getResources(self):
        return {
            "qty_core": self.qty_core,
            "cpu_usage": self.cpu_usage,
            "free_ram": self.free_ram,
            "free_disk": self.free_disk,
            "os_name": self.os_name
        }

    def setIsOnline(self, is_online):
        self.is_online = is_online
    
    def __str__(self):
        age = round(time.time() - self.last_seen, 1)
        return (
            f"{self.ip}:{self.tcp_port} | MAC={self.mac} | "
            f"Última mensagem: '{self.last_msg}' | {age}s atrás | Online: {self.is_online} | "
            f"SO: {self.os_name} | "
            f"Núcleos: {self.qty_core} | "
            f"CPU: {self.cpu_usage}% | "
            f"RAM livre: {self.free_ram}GB | "
            f"Disco livre: {self.free_disk}GB"
        )


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


    # -----------------------------------------------
    # ENVIA REQUISIÇÕES COM TCP PARA CLIENTE
    # -----------------------------------------------
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
    # VERIFICA CLIENTES ONLINE/OFFLINE
    # -----------------------------------------------
    def verify_clients(self):
        while True:
            time.sleep(VERIFY_CLIENT)
            for cli in self.clientes:
                cliente = self.clientes[cli]
                if (cliente.getAge() > BROADCAST_DELAY):
                    cliente.setIsOnline(False)
    
    # -----------------------------------------------
    # CONTA OS CLIENTES ONLINE/OFFLINE
    # -----------------------------------------------
    def count_online_offline(self):
        n_online = 0
        n_offline = 0
        for cli in self.clientes:
            cliente = self.clientes[cli]
            if cliente.getIsOnline(): n_online += 1
            else: n_offline += 1

        return {
            "n_online": n_online,
            "n_offline": n_offline
        }
    
    # -----------------------------------------------
    # REALIZA A MÉDIA DOS RECURSOS DOS CLIENTES
    # -----------------------------------------------
    def avg_resources(self):
        total_qty_core =  0
        total_cpu_usage = 0
        total_free_ram = 0
        total_free_disk = 0
        total_qty_windows = 0
        total_qty_linux = 0
        qty_clients = 0

        for cli in self.clientes.values():
            if not cli.is_online:
                continue

            total_free_ram += cli.free_ram
            total_free_disk += cli.free_disk
            total_cpu_usage += cli.cpu_usage
            total_qty_core += cli.qty_core
            qty_clients += 1

            if cli.os_name == "Windows": total_qty_windows += 1
            elif cli.os_name == "Linux": total_qty_linux += 1
        
        if qty_clients == 0:
            return None
        
        return {
            "avg_free_ram": round(total_free_ram / qty_clients, 2),
            "avg_free_disk": round(total_free_disk / qty_clients, 2),
            "avg_cpu_usage": round(total_cpu_usage / qty_clients, 2),
            "avg_qty_core": round(total_qty_core / qty_clients, 2),
            "avg_windows": round(total_qty_windows / qty_clients, 2),
            "avg_linux": round(total_qty_linux / qty_clients, 2),
        }


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
                data = response.split(";")
                resources = {}
                print(data)
                for i in data[2:]:
                    local_key, value = i.split("=") 
                    resources[local_key] = float(value)
                resources["os_name"] = data[1] 
                    
                self.clientes[key].updateResources(resources)   
        
        except Exception as e:
            print(f"[Erro] Erro de conexão TCP: {e}\n")
    
    def list_clients(self):
        for ip_address, tcp_port in self.clientes:
            print(f"{ip_address}:{tcp_port} -> {self.clientes[(ip_address, tcp_port)]}")
    
    def menu(self):
        while True:
            os_name = ""
            if (psutil.WINDOWS): os_name = "Windows"
            elif (psutil.LINUX): os_name = "Linux"
            elif (psutil.MACOS): os_name = "Mac OS"

            print(f"\n=== MENU SERVIDOR - ({os_name})===")
            opcoes = "1 - Listar clientes\n"
            opcoes += "2 - Solicitar MAC de um cliente via TCP\n" 
            opcoes += "3 - Solicitar MAC de todos os clientes via TCP\n" 
            opcoes += "4 - Solicitar dados dos recursos de um cliente via TCP\n" 
            opcoes += "5 - Solicitar dados dos recursos de todos os clientes via TCP\n" 
            opcoes += "0 - Sair\n"
            print(opcoes)
            op = input("> ")

            match op:
                case "1":
                    os.system("cls")
                    print("\n--- Clientes ---")
                    clients_on_off = self.count_online_offline()
                    print(f"Onlines: {clients_on_off["n_online"]} | Offlines: {clients_on_off["n_offline"]}")
                    avg = self.avg_resources()

                    print(
                        f"Média de RAM livre: {avg['avg_free_ram']}GB | "
                        f"Média de disco livre: {avg['avg_free_disk']}GB | "
                        f"Média de uso de CPU: {avg['avg_cpu_usage']}% | "
                        f"Qtd média de núcleos: {avg['avg_qty_core']}"
                    )

                    print(
                        f"Windows: {avg['avg_windows']} | "
                        f"Linux: {avg['avg_linux']}"
                    )

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
                    self.ask_me_resources((ip_address, tcp_port))
                    print(f"[Sucesso] Recursos do cliente {ip_address}:{tcp_port} recebidos")

                case "5":
                    try:
                        for key in self.clientes:
                            self.ask_me_resources(key)
                        print(f"[Sucesso] Recursos dos clientes recebidos")
                    except Exception as e:
                        print(f"[Erro] Erro: {e}")

                case "0":
                    exit()

                case _:
                    print("[Erro] Opção inválida")

    def start(self):
        threading.Thread(target=self.listen_broadcast, daemon=True).start()
        threading.Thread(target=self.verify_clients, daemon=True).start()
        threading.Thread(target=self.count_online_offline, daemon=True).start()
        self.menu()
                
if __name__ == "__main__":
    Servidor().start()