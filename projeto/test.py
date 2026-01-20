import psutil
import threading, time
# connections = psutil.net_connections()

# lista = []
# for con in connections:
#     info_conn = {
#         "status": con[5],
#         "address": con[3],
#         "family": con[1]
#     }
#     lista.append(info_conn)


# for i in lista:
#     print(f"{i}\n")

# interfaces_addrs = psutil.net_if_addrs()
# interfaces_stats = psutil.net_if_stats()
# lista_interfaces = []

# for i in interfaces_addrs:
#     print(f"{i}: {interfaces_addrs[i]}\n")

# for i in interfaces_addrs: 
#     for j in interfaces_stats:
#         if (i == j):
#             info = {
#                 "type": i,
#                 "address": interfaces_addrs[i][1].address,
#                 "status": interfaces_stats[j].isup
#             }
#             lista_interfaces.append(info)

# print(lista_interfaces)

print(time.time())
