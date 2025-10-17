class IPAddress:
    rede = str
    broadcast = str
    prefixo = str

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
        octetos = mascara.split(".")
        for o in octetos:
            n = int(o)
            mask_in_binry += f"{n:b}"
            
        # 2 - Faz a contagem dos números 1
        prefixo = 0
        for i in mask_in_binry:
            if (i == "1"):
                prefixo += 1

        self.prefixo = prefixo

        self.calcula_broadcast()
        self.calcula_rede()

    def calcula_rede(self):
        # CONVERTE ENDEREÇO EM LISTA
        lista_octetos_addr = list(map(int, self.endereco.split(".")))
        
        # CONVERTE MÁSCARA EM LISTA
        lista_octetos_mask = list(map(int, self.mascara.split(".")))

        # CALCULA A REDE
        rede = ""
        for i in range(4):
            n = lista_octetos_addr[i] & lista_octetos_mask[i]
            rede += str(n)
            rede += "."
        
        self.rede = rede[:-1]

    def calcula_broadcast(self):
        lista_octetos_mask = list(map(int, self.mascara.split(".")))
        lista_octetos_addr = list(map(int, self.endereco.split(".")))

        # INVERTE A MÁSCARA
        mask_invertida = []
        for oct_mask in lista_octetos_mask:
            n = oct_mask ^ 255 # XOR
            mask_invertida.append(n)

        broad = ""
        for i in range(4):
            n = lista_octetos_addr[i] | mask_invertida[i] # OR
            broad += str(n)
            broad += '.'
        
        self.broadcast = broad[:-1]

    def broadcast(self):
        return self.broadcast
    
    def rede(self):
        return self.rede

    def pertence_a_rede(self, rede_alvo):
        lista_mask = list(map(int, self.mascara.split(".")))
        lista_rede_alvo = list(map(int, rede_alvo.split(".")))

        rede = ""
        for i in range(4):
            n = str(lista_mask[i] & lista_rede_alvo[i])
            rede += n
            rede += '.'
        rede = rede[:-1] # REMOVE O ÚLTIMO PONTO DA STRING

        return self.rede == rede
            


ip = IPAddress("176.16.40.30", "255.255.192.0")
print(ip)                                       
print(ip.rede)                                  
print(ip.broadcast)                             
print(ip.pertence_a_rede("176.16.40.200"))       
print(ip.pertence_a_rede("176.16.192.0"))        