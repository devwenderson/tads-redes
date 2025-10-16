"""
DEFINIR O ALCANCE DA REDE
  1 - Converter os octetos para binário
  2 - Fazer a contagem de números 1
"""

class IPAdress:
    __rede = str
    __broadcast = str
    __prefixo = str

    def __init__(self, endereco, mascara):
        self.setEndereco(endereco)
        self.setMascara(mascara)
    
    def __str__(self):
        data = ""
        data += f"{self.__endereco}/{self.__prefixo}"
        return data
    
    def setEndereco(self, endereco):
        self.__endereco = endereco
    
    def setMascara(self, mascara):
        self.__mascara = mascara

        # CALCULA O PREFIXO DA REDE
        mask_in_binry = ""
        octetos = mascara.split(".")
        for o in octetos:
            n = int(o)
            mask_in_binry += f"{n:b}"
        
        prefixo = 0
        for i in mask_in_binry:
            if (i == "1"):
                prefixo += 1

        self.__prefixo = prefixo

    def getEndereco(self):
        return self.__endereco

    def getMascara(self):
        return self.__mascara

    def rede(self):
        # CONVERTE ENDEREÇO EM LISTA
        octetos_endereco = self.__endereco.split(".")
        lista_octetos_addr = list(map(int, octetos_endereco))
        
        # CONVERTE MÁSCARA EM LISTA
        octetos_mascara = self.__mascara.split(".")
        lista_octetos_mask = list(map(int, octetos_mascara))

        # CALCULA A REDE
        rede = []
        for i in range(4):
            calculo = lista_octetos_addr[i] & lista_octetos_mask[i]
            rede.append(calculo)
        
        rede = f"{rede[0]}.{rede[1]}.{rede[2]}.{rede[3]}"
        return rede

    def calcula_broadcast(self):
        pass

    def pertence_a_rede(self, rede):
        pass

ip = IPAdress("10.0.15.25", "255.255.254.0")
print(ip)
print(ip.rede())