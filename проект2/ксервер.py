# import socket
# import random
# import as
#
# HOST = (socket.gethostname(),10000)
#
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# s.bind(HOST)
# s.listen()
# print("слушаю гандона")
#
# while True :
#     conn,addr = s.accept()
#     print("подключен гандон:", addr)
#     ID = str(random.randint(0, 100000))
#     while True :
#         data = conn.recv(1024)
#         if not data :
#             break
#         if data.decode("UTF-8") == "connect":
#             res2 = ID.encode()
#             conn.send(res2)
#
#     conn.close()


import sys, asyncio,random


async def handle_client(reader, writer):
    print('New client connected...')
    line = str()

    while line.strip() != 'quit':
        line = (await reader.readline()).decode('utf8') # сообщение от клиента
        if line.strip() == '' : continue
        print(f'Received: {line.strip()}')


        if line.strip() == "connect" :
            player_ID = str(random.randint(10000, 1000000))
            writer.write(player_ID.encode())


        if line.strip() == "create_room":
            room_id = str(random.randint(10000, 1000000))

            print(room_id)
            players_room={room_id:[{player_ID:writer},]}
            print(players_room)
            writer.write(room_id.encode())
            print("комната создана")

        if line.strip() == "takken_id":
            writer.write(str(room_id).encode())

        if line.strip() == f"join_{room_id}": #возвращение от клиента
            players_room[room_id].append({player_ID:writer})
            print("213123123123")
            for i in players_room[room_id]:
                for j in players_room[room_id][i] :
                    print(j)
                    print(players_room)

                    writer.write("оба игрока подключились к комнате".encode()) # добавить обмен айдишниками



    writer.close()
    print('Client disconnected...')

async def run_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    print(f'Listening on {host}:{port}...')
    async with server:
        await server.serve_forever()

asyncio.run(run_server(host='localhost', port=10000))