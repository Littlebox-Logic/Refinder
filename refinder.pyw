from os import _exit
from sys import platform
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from cinterface import run_find
import ctypes
import time

root = Tk()
root.title("Littlebox Refinder | 就绪")
root.geometry("800x500")
root.resizable(width=False, height=False)

if platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass

ctrl_zone = Frame(master = root, height = 2)

e1text = StringVar()
Label(master = ctrl_zone, text = "关键词").grid(row = 0, column = 0, sticky = "w")
e1 = Entry(ctrl_zone, textvariable = e1text)
e1.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = "w")

e2text = StringVar()
Label(master = ctrl_zone, text = "查找范围").grid(row = 0, column = 2, padx = 10, sticky = "w")
e2 = Entry(ctrl_zone, textvariable = e2text)
e2.grid(row = 0, column = 3, padx = 10, pady = 5, sticky = "w")

stat = Label(master = ctrl_zone, text = "状态: 就绪", foreground = "#00FF00")
stat.grid(row = 1, column = 0, sticky = "w", columnspan = 3)

ctrl_zone.pack(side = TOP, padx = 5, pady = 5, fill = BOTH)

display_zone = Frame(root)
display_zone.place(x = 0, y = 80, width = 800, height = 400)
scrollbar = Scrollbar(display_zone)
scrollbar.pack(side = RIGHT, fill = Y)
lists = Treeview(display_zone, columns = ('c1', 'c2', 'c3'), show = "headings", yscrollcommand = scrollbar.set)
scrollbar.config(command = lists.yview)

lists.column('c1', width = 550)
lists.column('c2', width = 120, anchor = "center")
lists.column('c3', width = 100, anchor = "center")
lists.heading('c1', text = "目标路径")
lists.heading('c2', text = "目标类型")
lists.heading('c3', text = "模糊后缀")

lists.bind("<Control-Key-c>", lambda event:lists.event_generate('<<Copy>>'))
lists.bind("<Control-Key-C>", lambda event:lists.event_generate('<<Copy>>'))

lists.pack(side = LEFT, fill = BOTH)

signal = False

def find():
    global signal
    if signal:
        return None
    pattern = e1.get()
    types = {'D': "目录", 'F': "文件", 'L': "链接", 'U': "未知"}
    root.title("Littlebox Refinder | 删除记录中...")
    stat.config(text = "状态: 删除记录中...")
    for item in lists.get_children():
        lists.delete(item)
    stat.config(text = "状态: 查找中...")
    root.title(''.join(("Littlebox Refinder | ", "查找中 - \"", pattern, '"')))
    signal = True
    start_time = time.time()
    results = run_find(e2.get(), pattern)
    end_time = time.time()
    signal = False
    stat.config(text = "状态: 查找完成 | 耗时: %fs" % (end_time - start_time))
    root.title(''.join(("Littlebox Refinder | ", "查找完成 - \"", pattern, '"', " 耗时: %fs" % (end_time - start_time))))
    if results[0] == []:
        lists.insert('', 'end', values = ("无匹配项", "无信息", "是" if results[1] else "否"))
    else:
        for each in results[0]:
            lists.insert('', 'end', values = (each[0], types[each[1]], "是" if results[1] else "否"))

Button(master = ctrl_zone, text = "查找", command = lambda:Thread(target = find).start()).grid(row = 0, column = 4, padx = 10, pady = 5, sticky = 'e')

root.bind("<Return>", lambda event:Thread(target = find).start())

root.protocol("WM_DELETE_WINDOW", lambda:_exit(0))
root.mainloop()
