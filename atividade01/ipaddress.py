"""
1 - Para calcular o endereço de rede:
    Endereço HOST (AND) Máscara

2 - Para calcular o broadcast:
    Inverso da Máscara (OR) Endereço HOST
"""


class IPAddress:
    rede = str
    broadcast = str
    prefixo = str
    endereco = str

    def __init__(self, endereco: str, mascara: str):
        self.setEndereco(endereco)
        self.setMascara(mascara)
    
    def __str__(self):
        data = f"{self.endereco}/{self.prefixo}"
        return data
    
    def setEndereco(self, endereco):
        self.endereco = endereco
    
    def setMascara(self, mascara):
        self.mascara = mascara

        # -------- CALCULA O PREFIXO DA REDE --------

        # 1 - Converte os octetos para binário 
        mask_in_binry = ""
        for oct in mascara.split("."):
            mask_in_binry += format(int(oct), "08b")
            
        # 2 - Faz a contagem dos números 1
        prefixo = 0
        for i in mask_in_binry:
            prefixo = prefixo + 1 if i == '1' else prefixo + 0

        self.prefixo = str(prefixo)

        self.calcula_broadcast()
        self.calcula_rede()

    def calcula_rede(self):
        addr_bin = ""
        for i in self.endereco.split("."):
            addr_bin += format(int(i), "08b")
        
        mask_bin = ""
        for i in self.mascara.split("."):
            mask_bin += format(int(i), "08b")
        
        addr_int = int(addr_bin, 2)
        mask_int = int(mask_bin, 2)

        rede_int = addr_int & mask_int
        rede_bin = format(rede_int, "032b")

        rede = ""
        for i in range(0, 32, 8):
            rede += str(int(rede_bin[i:i+8], 2)) + '.'
        rede = rede[:-1]

        self.rede = rede

    def calcula_broadcast(self):

        addr_bin = ""
        for i in self.endereco.split("."):
            addr_bin += format(int(i), "08b")
        
        mask_bin = ""
        for i in self.mascara.split("."):
            mask_bin += format(int(i), "08b")
        
        addr_int = int(addr_bin, 2)
        mask_int = int(mask_bin, 2)

        mask_invert = format(mask_int ^ 4294967295, "032b")

        broad_int = addr_int | int(mask_invert, 2)
        broad_bin = format(broad_int, "032b")
        broad = ""
        for i in range(0, 32, 8):
            broad += str(int(broad_bin[i:i+8], 2)) + "."
        broad = broad[:-1]

        self.broadcast = broad

    def pertence_a_rede(self, rede_alvo):
        mask_bin = ""
        for i in self.mascara.split("."):
            mask_bin += format(int(i), "08b")
        
        rede_alvo_bin = ""
        for i in rede_alvo.split("."):
            rede_alvo_bin += format(int(i), "08b")

        mask_int = int(mask_bin, 2)
        rede_alvo_int = int(rede_alvo_bin, 2)

        rede_int = mask_int & rede_alvo_int
        rede_bin = format(rede_int, "032b")
        rede = ""

        for i in range(0, 32, 8):
            rede += str(int(rede_bin[i:i+8], 2)) + "."

        return self.rede == rede[:-1]
    
    def broadcast(self):
        return self.broadcast
    
    def rede(self):
        return self.rede
            

ip = IPAddress("176.16.192.30", "255.255.192.0")
print(f"Endereço com prefixo: {ip}")                                       
print(f"Endereço Rede: {ip.rede}")                                  
print(f"Broadcast: {ip.broadcast}")
r = "176.16.40.200"                             
print(f"{r} pertence a {ip.rede}? {ip.pertence_a_rede(r)}")
r2 = "176.16.192.0"       
print(f"{r2} pertence a {ip.rede}? {ip.pertence_a_rede(r2)}")        