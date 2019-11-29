import tkinter as tk
import tkinter.font as font
import random
import asyncio


def draw_text(text, font, x, y):
    # while True:
    # print("draw_text" + str(x))
    text.place(x=x, y=y)
    root.update()
    # root.update()
    # await asyncio.sleep(0.04)
    x -= 10
    if x >= -1000:
        root.after(100, draw_text(text, font, x, y))
    else:
        text.destroy()
        root.update()


root = tk.Tk()
root.wm_attributes("-transparent", True)
root.geometry("+1920+1080")
# root.wm_attributes("-transparent", root['bg'])

f = tk.Frame(root, width=1920, height=1080)
f.configure(bg="systemTransparent")
f.pack()

font = font.Font(root, family="System", size=100)


async def main():
    print("main")
    text = tk.Label(root, text="testcommentmessage", font=font)
    text.configure(bg="systemTransparent")
    await draw_text(text, font, 1000, random.uniform(150, 800))
    # t1 = threading.Thread(target=draw_text, args=(text, font))
    # t1.start


def main1():
    # root.mainloop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


main1()
