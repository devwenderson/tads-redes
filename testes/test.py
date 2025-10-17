class Operador:
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

    def srl(num):
        return '1' + num[:-1]
    
    def num_to_octetos(num):
        octetos = ""
        for i in range(32):
            octetos += "0"
        
        for i in range(num):
            octetos = "1" + octetos[:-1]
        
        lista_de_blocos = []
        for i in range(0, 32, 8):
            bloco = octetos[i:i+8]
            lista_de_blocos.append(bloco)
        
        # COLOCA NUMA STRING
        mask = ""
        for i in range(4):
            mask += lista_de_blocos[i]
            mask += "."
        
        print(mask[:-1])

octetos_endereco = ['255','255','254','0']
address_in_bnry = []
for e in octetos_endereco:
    n = int(e)
    address_in_bnry.append(f"{n:08b}")

"""
11111111.11111111.11110000.00000000
11111111.11111111.11111111.11111111

00000000.00000000.00001111.11111111
"""

Operador.num_to_octetos(19)