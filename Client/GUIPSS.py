# -*- coding: utf-8 -*-
import socket
from threading import Thread
import random
import tkinter as tk
import tkinter.font as font
import ssl
import yaml
from PIL import Image, ImageTk, ImageFile
import glob
import sys
import time


class Mainwindow(tk.Frame):

    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)


if __name__ == '__main__':
    yaml_dict = yaml.load(open('secret.yaml').read(), Loader=yaml.SafeLoader)
    user_name, user_pass, host, port = yaml_dict['username'], yaml_dict['password'],\
        yaml_dict['host'], int(yaml_dict['port'])

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    root = tk.Tk()
    root.title("1")
    root.geometry('300x400')
    w = 3840
    h = 2160
    img = []
    page = 1
    pagemax = len(glob.glob("Tmp/*"))
    for i in range(page, pagemax):
        tmp = Image.open(r"Tmp/page{}.png".format(i))
        tmp = tmp.resize((w, h))

        img.append(ImageTk.PhotoImage(tmp))

    # comment_font = font.Font(tk.sub_window, family="System", size=80)
    # labelimg = canvas.create_image(w / 2, h / 2, image=img[0])
    # th = Thread(target=rcv_comment)
    # th.setDaemon(True)
    # th.start()
    root.mainloop()
