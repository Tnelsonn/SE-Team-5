import socket
import scoreboard
import threading
import time

# Flag to indicate whether the receive_data thread should stop
stop_receive_thread_flag = False

def create_sockets():
    global sock_send, sock_receive, server_address_send, server_address_receive
    print('CREATING SOCKETS')
    # Create a UDP socket
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to port 7501 to receive data
    server_address_receive = ('localhost', 7501)

    # Server address to send data
    server_address_send = ('localhost', 7500)

    return sock_send, sock_receive, server_address_send, server_address_receive

def bind_sockets():
    sock_receive.bind(server_address_receive)
    #sock_send.bind(server_address_send) 

def receive_data():
    while not stop_receive_thread_flag:  # Check the flag before receiving data
        try:
            # Receive data
            data, address = sock_receive.recvfrom(4096)

            print('Received:', data.decode())

            # Process received data
            if b':' in data:
                # Player hit another player
                sender_id, hit_id = data.decode().split(':')
                if int(hit_id) == 53:
                    #Red base score
                    scoreboard.add_player_hits(sender_id,hit_id,100)
                    scoreboard.add_score(int(sender_id), 100)
                    transmit_data(sock_send, server_address_send, 100)
                elif int(hit_id) == 43:
                    #Green base scored
                    scoreboard.add_score(int(sender_id), 100)
                    scoreboard.add_player_hits(sender_id,hit_id,100)
                    transmit_data(sock_send, server_address_send, 100)
                elif int(sender_id) % 2 == int(hit_id) % 2:
                    # Player tagged themselves, transmit their own equipment ID
                    scoreboard.add_player_hits(sender_id,hit_id,-10)
                    scoreboard.add_score(int(sender_id), -10)
                    transmit_data(sock_send, server_address_send, sender_id)
                else:
                    # Player hit another player, transmit the hit player's equipment ID
                    scoreboard.add_player_hits(sender_id,hit_id,10)
                    scoreboard.add_score(int(sender_id), 10)
                    transmit_data(sock_send, server_address_send, hit_id)
        except socket.error as e:
            print("Socket error:", e)

    print("Stopping receive_data thread.")

# Send data
# logic to decide what data to send
# game start function to send '202'
def game_start(socket, address):
    socket.sendto(b'202', address)
    print('Game start')

# If the game ends, send '221' three times
# etc.
def game_end(socket, address):
    for _ in range(3):
        socket.sendto(b'221', address)
        print('Game end')

def transmit_data(socket, address, id):
    byte_data = str(id).encode()
    socket.sendto(byte_data, address)
    print('Transmitting')

def cleanup():
    sock_receive.close()

def stop_receive_thread():
    global stop_receive_thread_flag
    stop_receive_thread_flag = True

