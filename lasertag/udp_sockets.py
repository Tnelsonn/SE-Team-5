import socket

# Create a UDP socket
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to port 7501 to receive data
server_address_receive = ('localhost', 7501)
sock_receive.bind(server_address_receive)

# Server address to send data
server_address_send = ('localhost', 7500)

while True:
    # Receive data
    data, address = sock_receive.recvfrom(4096)

    # Process received data
    # Data logic
    # if data is '53', the red base has been scored
    # If data is '43', the green base has been scored
    if data == '53':
        print('Red base scored')
    elif data == '43':
        print('Green base scored')


    # Send data
    # logic to decide what data to send
    # game start function to send '202'
    def game_start():
        for _ in range(3):
            sock_send.sendto(b'202', server_address_send)
        

    # If the game ends, send '221' three times
    # etc.
    def game_end():
        for _ in range(3):
            sock_send.sendto(b'221', server_address_send)