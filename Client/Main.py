# -*- coding: utf-8 -*-
import socket
from threading import Thread
import random
import tkinter.font as font
import tkinter as tk
import time
import os
from PIL import Image, ImageTk, ImageFile
import glob
ImageFile.LOAD_TRUNCATED_IMAGES = True
root = tk.Tk()
root.state('zoomed')
# root.geometry("3840x2160")
# root.wm_attributes('-fullscreen', 1)
# root.tk.call("::tk::unsupported::MacWindowStyle",
#              "style", root._w, "plain", "none")
root.wm_attributes("-topmost", True)
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
img = []
for i in range(1, 20):
    tmp = Image.open(r"Tmp/page{}.png".format(i))
    tmp = tmp.resize((w, h))

    img.append(ImageTk.PhotoImage(tmp))

canvas = tk.Canvas(root, width=w, height=h)
labelimg = canvas.create_image(w / 2, h / 2, image=img[0])
canvas.pack()
font = tk.font.Font(root, family="System", size=80)
page = 1
pagemax = len(glob.glob("Tmp/*"))


class move_text:
    def __init__(self, canvas, comment):
        self.canvas = canvas
        self.text = self.canvas.create_text(
            w - 30, random.uniform(
                2.0, 8.0) * 100, text=comment, font=font)
        root.after(10, self.update)
        # root.update()

    def update(self):
        self.canvas.move(self.text, -1, 0)
        root.after(5, self.update)


def next(event):
    global page
    if pagemax - 1 > page:
        canvas.itemconfig(labelimg, image=img[page])
        page += 1


def prev(event):
    global page
    if 0 < page:
        canvas.itemconfig(labelimg, image=img[page])
        page -= 1


def rcv_comment():
    global canvas
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('45.76.215.122', 10023))
    idpass = os.environ.get('PSSID')
    print(idpass)
    s.sendall(bytes(idpass))
    while True:
        try:
            data = s.recv(1024)
            if len(data) != 0:
                comment = data.decode('utf-8')
                print("recv:" + comment)
                if comment == "認証エラー":
                    break
                move_text(canvas, comment)
            time.sleep(3)
        except KeyboardInterrupt:
            break
            s.close
        s.close
    s.close


if __name__ == '__main__':
    th = Thread(target=rcv_comment)
    th.start()
    root.bind("<Key-n>", next)
    root.bind("<Key-p>", prev)
    root.mainloop()
