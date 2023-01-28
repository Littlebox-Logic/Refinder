from os import _exit, path
from sys import platform
from threading import Thread
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from cinterface import run_find
import subprocess
import pyperclip
import ctypes
import time

root = Tk()
root.title("Littlebox Refinder | 就绪")
root.geometry("800x500")
root.resizable(width = False, height = False)

if platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass

root.iconbitmap(path.join(path.dirname(__file__), "logo_icon.ico"))
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
stat.grid(row = 1, column = 0, sticky = "w", columnspan = 5)

ctrl_zone.pack(side = TOP, padx = 5, pady = 5, fill = BOTH)

display_zone = Frame(root)
display_zone.place(x = 0, y = 80, width = 800, height = 400)
scrollbar = Scrollbar(display_zone)
scrollbar.pack(side = RIGHT, fill = Y)
lists = Treeview(display_zone, columns = ('c1', 'c2', 'c3', 'c4'), show = "headings", yscrollcommand = scrollbar.set)
scrollbar.config(command = lists.yview)

lists.column('c1', width = 460)
lists.column('c2', width = 65, anchor = "center")
lists.column('c3', width = 145, anchor = "center")
lists.column('c4', width = 100, anchor = "center")
lists.heading('c1', text = "目标路径")
lists.heading('c2', text = "目标类型")
lists.heading('c3', text = "修改日期")
lists.heading('c4', text = "文件大小")

def copy_obj(*event):
    for item in lists.selection():
        pyperclip.copy(lists.item(item,"values")[0])

def open_obj(*event):
    try:
        subprocess.run("explorer " + lists.item(lists.selection()[0], "values")[0], shell = True)
    except IndexError:
        pass

menu = Menu(root, tearoff = False)
menu.add_command(label = "复制(C)          Ctrl-C", command = copy_obj)
menu.add_command(label = "打开(O)          Ctrl-O", command = open_obj)

lists.bind("<Control-Key-c>", copy_obj())
lists.bind("<Control-Key-C>", copy_obj())
lists.bind("<Double-Button-1>", open_obj)
lists.bind("<Control-Key-O>", open_obj)
lists.bind("<Control-Key-o>", open_obj)
lists.bind("<Button-3>", lambda event:menu.post(event.x_root, event.y_root))

lists.pack(side = LEFT, fill = BOTH)

signal = False

def insert(results, types):
    for each in results[0]:
        lists.insert('', 'end', values = (each[0], types[each[1]], each[2], each[3]))

def find():
    global signal
    if signal:
        return None
    if len(e1.get()) > 260 or len(e2.get()) > 260:
        showinfo("长度限制", "搜索路径及关键词长度应小于260")
        return None
    for key in ('/', '\\', ':', '*', '?', '"', '<', '>', '|'):
        if key in e1.get():
            showwarning("非法字符", "关键词不应含有\n/ \\ : * ? \" < > |")
            return None
    pattern = e1.get()
    types = {'D': "目录", 'F': "文件", 'L': "链接", 'U': "未知"}
    root.title("Littlebox Refinder | 删除记录中...")
    stat.config(text = "状态: 删除记录中...", foreground = "#00FF00")
    root.after(0, lists.delete(*lists.get_children()))
    stat.config(text = "状态: 查找中...", foreground = "#00FF00")
    root.title(''.join(("Littlebox Refinder | ", "查找中 - \"", pattern, '"')))
    try:
        signal = True
        start_time = time.time()
        results = run_find(e2.get(), pattern)
        end_time = time.time()
    except Exception as reason:
        root.title("Littlebox Refinder | 致命错误")
        stat.config(text = "状态: 致命错误", foreground = "red")
        showerror("致命错误", "非法输入\n" + str(reason))
        signal = False
        return None
    signal = False
    stat.config(text = "状态: 查找完成 | 耗时: %fs | 匹配项: %d/%d" % (end_time - start_time, len(results[0]), results[1]), foreground = "#00FF00")
    root.title(''.join(("Littlebox Refinder | ", "查找完成 - \"", pattern, '"', " 耗时: %fs | 匹配项: %d/%d" % (end_time - start_time, len(results[0]), results[1]))))
    if results[0] == []:
        lists.insert('', 'end', values = ("无匹配项", "无信息", "", ""))
    else:
        root.after(0, insert, results, types)

Button(master = ctrl_zone, text = "查找", command = lambda:Thread(target = find).start()).grid(row = 0, column = 4, padx = 10, pady = 5, sticky = 'e')

root.bind("<Return>", lambda event:Thread(target = find).start())

root.protocol("WM_DELETE_WINDOW", lambda:_exit(0))
root.mainloop()
