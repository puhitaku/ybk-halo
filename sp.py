from contextlib import closing
import socket
import time
import sl4a

d = sl4a.Android()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    dt = 10
    d.startSensingTimed(2, dt)

    with closing(sock):
        while True:
            for i in range(1000):
                time.sleep(1/1000.0)
                d.eventClearBuffer()
                time.sleep(1/1000.0)
                e = d.eventPoll(1)
                if e.result is not None:
                    break
            s = d.sensorsReadAccelerometer().result
            z = str(s[2]).format(0).encode('utf-8')
            sock.sendto(z, ('192.168.11.58', 1234))
            print(z)
            time.sleep(dt/1000.0)

if __name__ == '__main__':
    main()