import pygame as pg
import socket, time, queue, os
from contextlib import closing
from threading import Thread

class SocketThread(Thread):
    def __init__(self, q):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.q = q
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        dt = 10

        with closing(self.sock):
            self.sock.bind(('192.168.11.58', 1234))
            while True:
                recv = self.sock.recv(100)
                print(recv)
                v = abs(float(recv))
                if v > 10:
                    v = 10
                self.q.put(v)
                time.sleep(dt/1000.0)

def main(q):
    w, h = 1280, 720

    pg.init()
    fps = pg.time.Clock()
    window = pg.display.set_mode((w, h), )

    col_d = pg.Color('0x381C00')
    col_l = pg.Color('0xFFF3AB')
    surface_d = pg.Surface((w, h))
    surface_l = pg.Surface((w, h), pg.SRCALPHA)
    surface_d.fill(col_d)

    srj = pg.image.load(os.path.join('data', 'srj.png')).convert_alpha()
    halo1 = pg.image.load(os.path.join('data', 'halo1.png')).convert_alpha()
    halo2 = pg.image.load(os.path.join('data', 'halo2.png')).convert_alpha()

    rect_srj = srj.get_rect()
    rect_srj.midtop = (w/2, 0)

    rect_halo1 = halo1.get_rect()
    rect_halo1.midtop = (w/2, 0)

    rect_halo2 = halo2.get_rect()
    rect_halo2.midtop = (w/2, 0)

    pg.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 1024)
    snd = pg.mixer.Sound(os.path.join('data', 'buddha.wav'))

    z = [0.0 for i in range(0, 10)]
    i = 0
    t = 0

    while True:
        if not q.empty():
            z = z[1:]
            z.append(q.get())
        
        z_ave = sum(z) / len(z)

        if z_ave > 2:
            if z_ave > 9:
                z_ave = 9
            col_l.a = int(255 / 7 * (z_ave - 2))
        else:
            col_l.a = 0

        if z_ave >= 8:
            if not pg.mixer.get_busy():
                snd.play()
        else:
            snd.stop()

        if t < 359:
            t += 1
        else:
            t = 0

        surface_l.fill(col_l)
        surface_d.fill(col_d)

        #_halo1 = pg.transform.rotate(halo1, t)
        #rect_halo1 = _halo1.get_rect()
        #rect_halo1.center = (0, h/2)

        for event in pg.event.get():
            pass

        window.blit(surface_d, (0, 0))
        window.blit(surface_l, (0, 0))
        
        if z_ave > 8:
            window.blit(halo1, rect_halo1)
            window.blit(halo2, rect_halo2)
        window.blit(srj, rect_srj)
        pg.display.update()
        fps.tick(60)

        


if __name__ == '__main__':
    q = queue.Queue()
    t = SocketThread(q)
    t.daemon = True
    t.start()
    main(q)