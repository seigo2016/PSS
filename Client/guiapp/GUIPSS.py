# -*- coding: utf-8 -*-
import eel
from threading import Thread
import socket
import ssl
import yaml
import tkinter as tk
import random
from PIL import Image, ImageTk, ImageFile
import glob
import tkinter.font as font
import sys


class CommentManager:
    def __init__(self, canvas):
        self.canvas_text_list = []
        self.canvas = canvas
        root.after(1, self.update)

    def add_text(self, comment):
        text = self.canvas.create_text(
            w, random.uniform(2.0, 18.0) * 100, text=comment, font=comment_font)
        self.canvas_text_list.append(text)

    def update(self):
        new_list = []
        for canvas_text in self.canvas_text_list:
            self.canvas.move(canvas_text, -15, 0)
            x, y = self.canvas.coords(canvas_text)
            if x > -10:
                new_list.append(canvas_text)
            else:
                self.canvas.delete(canvas_text)
        self.canvas_text_list = new_list
        root.after(20, self.update)


def next(event):
    global page
    if pagemax - 1 > page:
        canvas.itemconfig(labelimg, image=img[page])
        page += 1


def prev(event):
    global page
    if 0 <= page:
        canvas.itemconfig(labelimg, image=img[page])
        page -= 1


def end(event):
    sys.exit()


def status_message():
    eel.status(message)
    return


def rcv_comment(user_name, user_pass):
    global message
    global flg
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_verify_locations('server.pem')
    conn = context.wrap_socket(socket.socket(socket.AF_INET),
                               server_hostname=host)
    conn.connect((host, port))
    idpass = f"{user_name}:{user_pass}".encode()
    conn.sendall(idpass)
    # manager = CommentManager(canvas)
    while True:
        try:
            message = ""
            data = conn.recv(1024)
            comment = data.decode('utf-8')
            if len(comment):
                print(comment)
                if comment == "認証エラー":
                    message = "Auth error"
                    break
                elif comment == "接続完了":
                    message = "Connected"
                    flg = False
                    # manager.add_text(comment)
                if len(message):
                    status_message()
        except KeyboardInterrupt:
            break
    conn.close()


@eel.expose
def app_connect(user_name, user_pass):
    rcv_comment(user_name, user_pass)


def web():
    eel.init("web")
    eel.start("main.html")


if __name__ == '__main__':
    flg = True
    message = ""
    yaml_dict = yaml.load(open('../secret.yaml').read(),
                          Loader=yaml.SafeLoader)
    host, port = yaml_dict['host'], int(yaml_dict['port'])
    th = Thread(target=web)
    th.setDaemon(True)
    th.start()
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    root = tk.Tk()
    root.geometry("1920x1080")
    w = int(1920/2)
    h = int(1080/2)
    img = []
    page = 1
    pagemax = len(glob.glob("../Tmp/*"))
    for i in range(page, pagemax):
        tmp = Image.open(r"../Tmp/page{}.png".format(i))
        tmp = tmp.resize((w, h))
        img.append(ImageTk.PhotoImage(tmp))
    canvas = tk.Canvas(root, width=w, height=h)
    canvas.pack()
    comment_font = font.Font(root, family="System", size=80)
    labelimg = canvas.create_image(w / 2, h / 2, image=img[0])
    root.bind("<Key-n>", next)
    root.bind("<Key-q>", end)
    root.bind("<Key-p>", prev)
    while flg:
        pass
    root.mainloop()
