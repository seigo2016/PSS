# -*- coding: utf-8 -*-
import socket
from threading import Thread
import random
import tkinter as tk
import tkinter.font as font
import time
import ssl
import yaml
from PIL import Image, ImageTk, ImageFile
import glob

yaml_dict = yaml.load(open('secret.yaml').read(), Loader=yaml.SafeLoader)
user_name, user_pass, host, port = yaml_dict['username'], yaml_dict['password'],\
    yaml_dict['host'], int(yaml_dict['port'])

ImageFile.LOAD_TRUNCATED_IMAGES = True

root = tk.Tk()
root.geometry("3840x2160")
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
comment_font = font.Font(root, family="System", size=80)
page = 1
pagemax = len(glob.glob("Tmp/*"))


class move_text:
    def __init__(self, canvas, comment):
        self.canvas = canvas
        self.text = self.canvas.create_text(
            w, random.uniform(
                2.0, 8.0) * 100, text=comment, font=comment_font)
        root.after(1, self.update)

    def update(self):
        self.canvas.move(self.text, -5, 0)
        root.after(1, self.update)


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


def rcv_comment():
    global canvas
    context = ssl.create_default_context()
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    context.check_hostname = False
    conn = context.wrap_socket(socket.socket(socket.AF_INET),
                               server_hostname=host)
    conn.connect((host, port))
    idpass = "{}:{}".format(user_name, user_pass).encode()
    conn.sendall(idpass)
    while True:
        try:
            data = conn.recv(1024)
            if len(data) != 0:
                comment = data.decode('utf-8')
                print("recv:" + comment)
                if comment == "認証エラー":
                    break
                move_text(canvas, comment)
            time.sleep(3)
        except KeyboardInterrupt:
            break
            conn.close
        conn.close
    conn.close


if __name__ == '__main__':
    th = Thread(target=rcv_comment)
    th.start()
    root.bind("<Key-n>", next)
    root.bind("<Key-p>", prev)
    root.mainloop()
