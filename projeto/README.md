# Projeto com Sockets
Esse projeto está em desenvolvimento com a linguagem python. o objetivo dessa atividade é trabalhar os conceitos de: 
- `Sockets` 
- `Threads` 
- `Comunicação TCP e UDP`
- `Transmissão de dados pela rede`
- `Localização de computadores a partir da rede`

## Bibliotecas python utilizadas
- sockets
- threading
- uuid
- time
- random
- psutil
- datetime
- os
- json

## O que fazer
### 1. OBJETIVO

Construir um sistema cliente/servidor para inventário e monitoramento de computadores em rede, com
descoberta automática, coleta de métricas, consolidação de dados e ação remota segura, por meio de
comandos administrativos ou integração com ferramenta padrão de controle remoto.

---

### 2. FUNCIONALIDADES (4,0 PONTOS)

#### 2.1 Coleta por Cliente (2,0 pontos)

* [x] Quantidade de processadores / núcleos (0,4)
* [x] Memória RAM livre (0,4)
* [x] Espaço em disco livre (0,4)
* [ ] IPs das interfaces de rede, incluindo status (UP/DOWN) e tipo (loopback, ethernet, wifi) (0,4)
* [x] Identificação do sistema operacional (0,4)

---

#### 2.2 Servidor / Consolidação (2,0 pontos)

- [x] Dashboard em terminal ou interface gráfica simples com lista de clientes, última atualização, sistema operacional e IP principal (0,5)

- [x] Consolidação dos dados com cálculo de média simples e contagem de clientes online e offline. Cliente offline é aquele que não responde ao mecanismo de hello por mais de 30 segundos (0,5)

- [x] Funcionalidade de detalhamento de um cliente selecionado (0,5)

- [x] Exportação de relatórios do consolidado geral e de um cliente específico nos formatos CSV ou JSON (0,5)

---

### 3. REQUISITOS PRINCIPAIS (4,0 PONTOS)

- [x] Arquitetura Cliente/Servidor (1,0)

- [x] Descoberta automática de clientes na LAN utilizando técnicas como broadcast, multicast ou mensagens periódicas de hello (1,0)

- [x] Uso de sockets puros (TCP e/ou UDP) para comunicação do protocolo desenvolvido (1,0)

- [x] Utilização do paradigma de Orientação a Objetos, com organização clara e modular do código (1,0)

---

### 4. SEGURANÇA (1,0 PONTO)

- [ ] Comunicação segura utilizando criptografia e mecanismos de integridade ponta a ponta (0,5)

- [ ] Autenticação dos clientes e controle de acesso por perfil (0,3)

- [ ] Auditoria no servidor, registrando ações executadas, responsáveis e data/hora (0,2)

---

### 5. BÔNUS (ATÉ 2,0 PONTOS)

- [ ] Controle remoto do mouse do cliente (1,0)

- [ ] Controle remoto do teclado do cliente (1,0)

## Referências
- [Sockets - python](https://docs.python.org/3/library/socket.html)
- [Threading - python](https://docs.python.org/3/library/threading.html)
- [Uuid - python](https://docs.python.org/3/library/uuid.html)
- [random - python](https://docs.python.org/3/library/random.html)
- [time - python](https://docs.python.org/3/library/time.html)
- [Código base das classes usadas no projeto](https://github.com/devwenderson/RedesDeComputadores/tree/main/material_de_apoio/SideQuests/LocalizadorComputadores)