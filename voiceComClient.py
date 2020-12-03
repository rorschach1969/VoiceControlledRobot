#Ben Popernik
#Sophomore Lab in Applied Computing
#Raspberry Pi Final Project
#voiceComClient.py

import aiy.audio # the following imports are for the Google cloudspeech api
import aiy.cloudspeech
import aiy.voicehat
import socket

host = '<YOUR_ROBOT_IP>' #This is the ip address of the server located on the robot
port = 5560

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #The call used for sending text using socket
s.connect((host,port)) #connects to the server 


def main():
    #This function combines the voice recognition from google
    # and ties it to commands to be sent to the server
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('GET')
    recognizer.expect_phrase('BLINK')
    recognizer.expect_phrase('blink')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()

    while True:
        print('Press the button and speak')
        button.wait_for_press()
        print('Listening...')
        text = recognizer.recognize()
        
        if not text:
            print('Sorry, I did not hear you.') #If the mic couldn't understand
        elif text == 'exit': #This tells the server that you are leaving
            s.send(str.encode(text)) #sends 'exit' to the server
            break #stops the while loop and shuts down the program
        elif text == 'kill': #This shuts down the server and client at the same time
            s.send(str.encode(text))
            break
        else:
            print('You said "', text, '"') #Prints what was recorded by the microphone
            s.send(str.encode(text)) #sends the text to the server
            reply=s.recv(1024) #The bytes that are sent to the server 
            print(reply.decode('utf-8')) # The decoding key
            if 'turn on the light' in text: # the following are functions to control the light at the top of the 
                led.set_state(aiy.voicehat.LED.ON) #Voice box. This is good to test if the box and code are working
            elif 'turn off the light' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'goodbye' in text:
                break


if __name__ == '__main__':
    main() #This runs the program when it is opeaned

