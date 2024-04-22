import socket
import scoreboard

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
    while True:
        # Receive data
        data, address = sock_receive.recvfrom(4096)

        print('Received:', data.decode())

        # Process received data
        if b':' in data:
            # Player hit another player
            sender_id, hit_id = data.decode().split(':')
            if hit_id == 53:
                #Red base score
                scoreboard.add_score(sender_id, 100)
                transmit_data(sock_send, server_address_send, 100)
                
            elif hit_id == 43:
                #Green base scored
                scoreboard.add_score(sender_id, 100)
                transmit_data(sock_send, server_address_send, 100)
                
            elif sender_id == hit_id:
                # Player tagged themselves, transmit their own equipment ID
                scoreboard.add_score(sender_id, -10)
                transmit_data(sock_send, server_address_send, sender_id)
                
            else:
                # Player hit another player, transmit the hit player's equipment ID
                scoreboard.add_score(sender_id, 10)
                transmit_data(sock_send, server_address_send, hit_id)
            

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
    byte_data = id.encode()
    socket.sendto(byte_data, address)
    print('Transmitting')