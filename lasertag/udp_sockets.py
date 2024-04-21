import socket

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