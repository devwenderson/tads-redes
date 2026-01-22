import os, json
from datetime import datetime
import socket, threading, time, psutil
from models import ClienteInfo

BROADCAST_PORT = 50000
BROADCAST_DELAY = 25
VERIFY_CLIENT = 10

def list_to_dict(response):
    data = response.split(";")[1:]
    return dict(item.split("=") for item in data)

class Servidor:
    def __init__(self):
        self.clientes = {} # chave: (ip, tcp_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", BROADCAST_PORT))

    # -----------------------------------------------
    # ESCUTA BROADCASTS
    # -----------------------------------------------
    def listen_broadcast(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            mensagem = data.decode()
            ip = addr[0]

            if mensagem.startswith("DISCOVER_REQUEST"):
                data = list_to_dict(mensagem)
                tcp_port = data['port']
                key = (ip, int(tcp_port))

                # Salva cliente com chave composta (ip, tcp_port)
                if key not in self.clientes:
                    self.clientes[key] = ClienteInfo(ip, tcp_port, data['verificador'])
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

                resources = list_to_dict(response)
  
                for local_key in resources:
                    if local_key == 'os_name':
                        continue
                    resources[local_key] = float(resources[local_key])

                self.clientes[key].updateResources(resources)   
        
        except Exception as e:
            print(f"[Erro] Erro de conexão TCP: {e}\n")

# ---------------------------------------------------------
    # SELECIONA UM CLIENTE NA BASE DE DADOS
    # ---------------------------------------------------------
    def ask_me_the_client(self):
        try:
            os.system("cls")
            self.list_clients()
            data = input("Digite o endereço com a porta (Ex.: 222.222.222.222:2222): ")
            ip_address, tcp_port = data.split(":")
            return (ip_address, tcp_port)
        except Exception as e:
            print(f"[Erro] Erro: {e}\n")
    
    def list_clients(self):
        for ip_address, tcp_port in self.clientes:
            print(f"{self.clientes[(ip_address, tcp_port)]}")
    
    def show_resources_avg(self):
        if (len(self.clientes) == 0):
            print("Clientes não cadastrados")
            return
        
        avg = self.avg_resources()

        print(
            f"====================MÉDIAS=========================\n"
            f"Média de RAM livre: {avg['avg_free_ram']}GB\n"
            f"Média de disco livre: {avg['avg_free_disk']}GB\n"
            f"Média de uso de CPU: {avg['avg_cpu_usage']}%\n"
            f"Qtd média de núcleos: {avg['avg_qty_core']}\n"
            f"Windows: {avg['avg_windows']} | Linux: {avg['avg_linux']}\n"
            f"===================================================\n"
        )

    def data_export_all_clients(self):
        if (len(self.clientes) <= 0):
            print("[Erro] Não há clientes")
            return

        clientes_to_json = [cliente.to_json() for cliente in self.clientes.values()]
        path = os.path.dirname(__file__)
        file_name = f"clientes-{datetime.now().strftime("%Y-%m-%d--%H-%M-%S")}"
        
        with open(f"{path}/exports/{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(clientes_to_json, f, indent=4, ensure_ascii=False)
    
    def data_export_single_client(self, key):
        if (len(self.clientes) <= 0):
            print("[Erro] Não há clientes")
            return

        cliente_to_json = self.clientes[key].to_json()
        print(cliente_to_json)
        
        path = os.path.dirname(__file__)
        file_name = f"cliente-{cliente_to_json['verificador']}"
        
        with open(f"{path}/exports/{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(cliente_to_json, f, indent=4, ensure_ascii=False)


    def menu(self):
        while True:
            os_name = ""
            if (psutil.WINDOWS): os_name = "Windows"
            elif (psutil.LINUX): os_name = "Linux"
            elif (psutil.MACOS): os_name = "Mac OS"

            hostname = socket.gethostname()
            my_ip = socket.gethostbyname(hostname)

            print(f"\n========== MENU SERVIDOR | Meu OS: ({os_name}) | Meu IP: {my_ip} | Porta do broadcast: {BROADCAST_PORT} ==========")
            opcoes = "1 - Listar clientes\n"
            opcoes += "2 - Solicitar MAC de um cliente via TCP\n" 
            opcoes += "3 - Solicitar MAC de todos os clientes via TCP\n" 
            opcoes += "4 - Solicitar dados dos recursos de um cliente via TCP\n" 
            opcoes += "5 - Solicitar dados dos recursos de todos os clientes via TCP\n" 
            opcoes += "6 - Exportar dados dos clientes para JSON\n" 
            opcoes += "7 - Exportar dados de UM cliente para JSON\n" 
            opcoes += "0 - Sair\n"
            print(opcoes)
            op = input("> ")

            match op:
                case "1":
                    os.system("cls")

                    # EXIBE AS MÉDIAS DOS RECURSOS
                    self.show_resources_avg()

                    print("--------------------Clientes--------------------")

                    # EXIBE CLIENTES ONLINE/OFFLINE
                    clients_on_off = self.count_online_offline()
                    print(f"\n====== Onlines: {clients_on_off["n_online"]} | Offlines: {clients_on_off["n_offline"]} ======\n")
                    
                    # EXIBE OS CLIENTES
                    self.list_clients()

                case "2":
                    ip_address, tcp_port = self.ask_me_the_client()
                    self.ask_me_tcp((ip_address, int(tcp_port)))

                case "3":
                    for key in self.clientes:
                        self.ask_me_tcp(key)

                case "4":
                    ip_address, tcp_port = self.ask_me_the_client()
                    self.ask_me_resources((ip_address, int(tcp_port)))
                    print(f"[Sucesso] Recursos do cliente {ip_address}:{tcp_port} recebidos")

                case "5":
                    try:
                        for key in self.clientes:
                            self.ask_me_resources(key)
                        print(f"[Sucesso] Recursos dos clientes recebidos")
                    except Exception as e:
                        print(f"[Erro] Erro: {e}")
                
                case "6":
                    try:
                        self.data_export_all_clients()
                        print("[Sucesso] Dados exportados com sucesso!")
                    except Exception as e:
                        print(f"[Erro] Erro: {e}")

                case "7":
                    try:
                        ip_address, tcp_port = self.ask_me_the_client()
                        self.data_export_single_client((ip_address, int(tcp_port)))
                        print("[Sucesso] Dados exportados com sucesso!")
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