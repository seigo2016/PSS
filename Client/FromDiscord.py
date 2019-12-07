# -*- coding: utf-8 -*-
from threading import Thread
from multiprocessing import Process, Value
import random
import tkinter.font as font
import tkinter as tk
import yaml
import discord
import ctypes
from PIL import Image, ImageTk, ImageFile
import glob
import sys

commentbody = Value(ctypes.c_char_p, ''.encode())
client = discord.Client()
sys.setrecursionlimit(10000)
ImageFile.LOAD_TRUNCATED_IMAGES = True

yaml_dict = yaml.load(open('secret.yaml').read(), Loader=yaml.SafeLoader)
token = yaml_dict['token']

# root.wm_attributes('-fullscreen', 1)
# root.tk.call("::tk::unsupported::MacWindowStyle",
#              "style", root._w, "plain", "none")


class move_text:
    def __init__(self, canvas, comment):  # 初回実行時はテキストと出現位置をセット
        self.canvas = canvas
        self.count = 0
        self.text = self.canvas.create_text(
            w + 200, random.uniform(
                2.0, 8.0) * 100, text=comment, font=comment_font)
        root.after(1, self.update)

    def update(self):  # 以降は左へ移動させていく
        self.count += 1
        self.canvas.move(self.text, -5, 0)
        if self.count * 5 <= w:  # 画面より左に出た場合削除
            root.after(1, self.update)
        else:
            self.canvas.delete(self.text)


def next(event):
    global page
    if pagemax - 1 > page:
        canvas.itemconfig(labelimg, image=img[page])
        page += 1


def prev(event):
    global page
    if 0 <= page:
        print(event.widget)
        canvas.itemconfig(labelimg, image=img[page])
        page -= 1


def main():
    global labelimg
    # p1 = Process(target=client.run, args=(token))
    # p1.start()
    pagemax = len(glob.glob("Tmp/*"))
    message = commentbody.value
    commentbody.value = "".encode()
    root = tk.Tk()
    root.geometry("3840x2160")
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
    # comment_font = font.Font(root, family="System", size=80)
    root.bind("<Key-p>", prev)
    root.bind("<Key-n>", next)

    root.mainloop()


@client.event
async def on_message(message):
    # move_text(canvas, message.content)
    with commentbody.get_lock():
        commentbody.value = message.content.encode()

if __name__ == '__main__':
    page = 1
    main()
