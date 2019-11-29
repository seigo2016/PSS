# -*- coding: utf-8 -*-
import socket
from multiprocessing import Array Pool, Process
from threading import Thread
import multiprocessing
import cv2
import random
import numpy as np
from PIL import ImageFont, ImageDraw, Image
# from collections import deque

# q = deque([[]], 100)
q = [[None, 0, 0] for i in range(50)]

width = 1600
height = 900


def rcv_comment():
    global q
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('45.76.215.122', 10023))
    s.sendall(b'seigo:password')
    while True:
        try:
            data = s.recv(1024)
            if len(data) != 0:
                comment = data.decode('utf-8')
                print("recv:" + comment)
                # print(type(comment))
                if comment == "認証エラー":
                    break
                else:
                    for i in range(len(q)):
                        if q[i][0] is None:
                            q[i] = [comment, 0, random.uniform(50, height)]
                            break
                        print(q)
        except KeyboardInterrupt:
            break
            s.close
        s.close
        # except Exception as e:
        #     print(e)
        #     print("エラー")
    s.close


def slide(list_q):
    font = ImageFont.truetype("./ipaexg.ttf", 64)
    page = 0
    img = cv2.imread('./Temp/test{}.png'.format(page))
    img = cv2.resize(img, dsize=(1920, 1080))
    for i in range(len(list_q)):
        if list_q[i][1] > 1800:
            list_q[i] = [None, 0, 0]
        elif list_q[i][0] is not None:
            print("comment:" + list_q[i][0])
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            draw.text((1600 - int(list_q[i][1]), int(list_q[i][2])),
                      list_q[i][0], font=font, fill=(0, 0, 0))
            list_q[i][1] += 7 * len(list_q[i][0])
            img = np.array(img_pil)
    return img


if __name__ == '__main__':
    q = [[None, 0, 0] for i in range(50)]
    # q = Array("b", [[None, 0, 0] for i in range(50)])
    thread1 = Thread(target=rcv_comment)
    thread1.setDaemon(True)
    # thread2 = Thread(target=slide)
    thread1.start()
    # thread2.start()
    while True:
        img = slide(q)
        cv2.namedWindow('screen', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(
            'screen', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("screen", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
