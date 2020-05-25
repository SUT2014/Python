import socket
import random

serverAddressPort = ("127.0.0.1", 5990)


def main():
    print("there is no spoon")
    udpclientsocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    for i in range(100):
        bytesToSend = str.encode(str(random.randint(10, 30)))
        print(i, bytesToSend)
        udpclientsocket.sendto(bytesToSend, serverAddressPort)
        #time.sleep(.1)


if __name__ == "__main__":
    main()