import socket

def create_sockets():
    global sock_send, sock_receive, server_address_send, server_address_receive
    print('CREATING SOCKETS')
    # Create a UDP socket
    sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send = 1
    sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to port 7501 to receive data
    server_address_receive = ('localhost', 7501)
    receive = 1
    sock_receive.bind(server_address_receive)

    # Server address to send data
    server_address_send = ('localhost', 7500)


def receive_data():
    while True:
        # Receive data
        data, address = sock_receive.recvfrom(4096)

        # Process received data
        # Data logic
        # if data is '53', the red base has been scored
        # If data is '43', the green base has been scored
        if data == b'53':
            print('Red base scored')
        elif data == b'43':
            print('Green base scored')

    # Send data
    # logic to decide what data to send
    # game start function to send '202'
def game_start():
    global sock_send, server_address_send
    for _ in range(3):
        sock_send.sendto(b'202', server_address_send)
        print('Game start')
        

    # If the game ends, send '221' three times
    # etc.
def game_end():
    global sock_send, server_address_send
    for _ in range(3):
        sock_send.sendto(b'221', server_address_send)
        print('Game end')