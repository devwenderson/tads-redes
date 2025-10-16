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
        
        print(lista_de_blocos)

octetos_endereco = ['255','255','254','0']
address_in_bnry = []
for e in octetos_endereco:
    n = int(e)
    address_in_bnry.append(f"{n:08b}")

print(address_in_bnry)