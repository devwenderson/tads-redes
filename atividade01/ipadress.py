"""
DEFINIR O ALCANCE DA REDE
  1 - Converter os octetos para binário
  2 - Fazer a contagem de números 1
"""
def dec_to_bin(dec):
    if dec == 0:
        return "00000000"
    bin = ""
    quo = dec
    while (quo != 0):
        resto = quo % 2
        bin = str(resto) + bin
        quo = quo // 2
    return bin

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
        octetos = list(map(int, mascara.split(".")))
        octetos = list(map(dec_to_bin, octetos))

        prefixo = 0
        for i in octetos:
            for j in i:
                if j == '1':
                    prefixo += 1

        self.__prefixo = prefixo
    
    def getEndereco(self):
        return self.__endereco

    def getMascara(self):
        return self.__mascara

    def calcula_rede(self):
        pass

    def calcula_broadcast(self):
        pass

    def pertence_a_rede(self, rede):
        pass

ip = IPAdress("192.168.0.12", "255.128.0.0")
ip.calcula_prefixo()
print(ip)