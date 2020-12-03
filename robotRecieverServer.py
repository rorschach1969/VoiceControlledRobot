# Ben Popernik
# Sophomore Lab in Applied Computing
# Raspberry Pi Final Project
# robotRecieverServer.py

#This uses the rrb2 library

import socket


from rrb2 import *

rr = RRB2()


host = ''
port = 5560

storedValue = "Hi There! Welcome to VoicePiBot"
function = "Next command"

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")

    try:
        s.bind((host,port))
    except socket.error as msg:
        print(msg) #Says that there was an error in the connection
    print("Socket bind complete.")
    return s

def setupConnection():
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def dataTransfer(conn):
    # function that allows to send and recieve data until told not to!
    while True:
        # Recieve the data
        data = conn.recv(1024) #recieve the data and the number is the bit rate
        data = data.decode('utf-8')
        # Split the data such that you separate the command
        #from the rest of the data.
        dataMessage = data.split(' ', 1)
        command = dataMessage[0]
        if command == 'get':
            reply = GET()
        elif command == 'repeat':
            reply = REPEAT(dataMessage)
        elif command == 'exit':
            print("Client has left")
            break
        elif command == 'kill':
            print("Server shutting down")
            s.close()
            break
        elif command == 'forward':
            print('Moving Forward')
            reply = forward()
        elif command == 'right':
            print('Turning Right')
            reply = rightTurn()
        elif command == 'left':
            print('Turning Left')
            reply = leftTurn()
        else:
            reply = 'Unknown Command'
        # Send the reply back to the client
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
    conn.close()


def GET():
    reply = storedValue
    return reply

def REPEAT(dataMessage):
    reply=dataMessage[1]
    return reply

#The following are the commands to control the robot


def forward():
    rr.forward(5,1)
    reply = function
    return reply

def rightTurn():
    rr.right(3,0.5)
    reply = function
    return reply

def leftTurn():
    rr.left(2,0.5)
    reply = function
    return reply

s = setupServer()

while True:
    try:
        conn = setupConnection() # This is used to broadcast a connecton
        dataTransfer(conn)
    except:
        break
    
                      

