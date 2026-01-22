import time
class ClienteInfo:
    def __init__(self, ip, tcp_port, verificador):
        self.verificador = verificador
        self.ip = ip
        self.tcp_port = tcp_port
        self.last_seen = time.time()
        self.last_msg = ""
        self.mac = None
        self.is_online = True
        self.qty_core =  0
        self.cpu_usage = 0
        self.free_ram = 0
        self.free_disk = 0
        self.os_name = ""
    
    def updateResources(self, resoucers_dict):
        self.qty_core =  resoucers_dict["qty_core"]
        self.cpu_usage = resoucers_dict["cpu_usage"]
        self.free_ram = resoucers_dict["free_ram"]
        self.free_disk = resoucers_dict["free_disk"]
        self.os_name = resoucers_dict["os_name"]

    def update(self, msg):
        self.last_msg = msg
        self.last_seen = time.time()
    
    def __str__(self):
        age = round(time.time() - self.last_seen, 1)
        return (
            f"ID: {self.verificador}\n"
            f"Endereço: {self.ip}:{self.tcp_port} | MAC={self.mac}\n"
            f"Última mensagem: '{self.last_msg}' | {age}s atrás\n" 
            f"Online: {self.is_online}\n"
            f"SO: {self.os_name}\n"
            f"Núcleos: {self.qty_core}\n"
            f"CPU: {self.cpu_usage}%\n"
            f"RAM livre: {self.free_ram}GB\n"
            f"Disco livre: {self.free_disk}GB\n"
        )
    
    # ---------- GETTERS ----------   
    def getAge(self):
        # TEMPO QUE PASSOU DESDE A ÚLTIMA MENSAGEM
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

    # ---------- SETTERS ----------
    def setIsOnline(self, is_online):
        self.is_online = is_online

    # ---------- JSON -----------
    def to_json(self):
        age = round(time.time() - self.last_seen, 1)

        return {
            "verificador": self.verificador,
            "network": {
                "ip": self.ip,
                "tcp_port": self.tcp_port,
                "mac": self.mac
            },
            "status": {
                "is_online": self.is_online,
                "last_seen": self.last_seen,
                "age_seconds": age,
                "last_msg": self.last_msg
            },
            "resources": {
                "os_name": self.os_name,
                "qty_core": self.qty_core,
                "cpu_usage": self.cpu_usage,
                "free_ram": self.free_ram,
                "free_disk": self.free_disk
            }
        }
    