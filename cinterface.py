from ctypes import *
from os import path, getcwd

engine = windll.LoadLibrary("./refinder_engine.dll")

class File_list(Structure):
    pass

class File_name(Array):
    _length_ = 261
    _type_ = c_char

File_list._fields_ = [\
    ("next", POINTER(File_list)), 
    ("file_type", c_char),
    ("file_name", File_name)]

engine.find.argtypes = [c_char_p, c_char_p]
engine.find.restype = POINTER(File_list)

def run_find(directory:str, pattern:str) -> list:
    '''Perform Find Operations.
    Usage: run_find(directory, pattern)
      e.g. run_find("C:\\", "main.c")
    Return:A list([(name_1, type_1), (name_2, type_2), ...]) and a if-fuzzy-search signal.
    File_Type:
        U -> Unknown  File;
        F -> Normal   File;
		L -> Symbolic Link;
        D -> Directory.
    '''
    table = []
    if len(directory) == 0 or directory == '\\':
        directory = getcwd()
    if directory[-1] != '\\':
        directory += '\\'
    try:
        target = engine.find(c_char_p(path.normpath(directory).encode('gbk')), c_char_p(pattern.encode('gbk')))
        signal = False
    except OSError:
        target = engine.find(c_char_p(path.normpath(directory).encode('gbk')), c_char_p(path.splitext(pattern)[0].encode('gbk')))
        signal = True
    while True:
        try:
            table.append((path.normpath(target.contents.file_name.decode('gbk')), target.contents.file_type.decode('gbk')))
            target = target.contents.next
        except ValueError as reason:
            if str(reason) != "NULL pointer access":
                raise ValueError("读取已缓存数据出现问题 请联系项目开发者: %s" % reason)
            break
    return table, signal
