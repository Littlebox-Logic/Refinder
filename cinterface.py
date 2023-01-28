from ctypes import *
from os import path, getcwd
from time import strftime, localtime

engine = windll.LoadLibrary(path.join(path.dirname(__file__), "refinder_engine.dll"))

class File_list(Structure):
    pass

File_list._fields_ = [\
    ("next", POINTER(File_list)),
    ("edit_time", c_longlong),
    ("file_size", c_longlong),
    ("file_name", c_char * 261),
    ("file_type", c_char)]

engine.find.argtypes = [c_char_p, c_char_p]
engine.find.restype = POINTER(File_list)
engine.return_files_count.restype = c_ulonglong

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
    target = engine.find(c_char_p(path.normpath(directory).encode('gbk')), c_char_p(pattern.encode('gbk')))
    while True:
        try:
            table.append((path.normpath(target.contents.file_name.decode('gbk')), target.contents.file_type.decode('gbk'), strftime("%Y/%m/%d %H:%M:%S", localtime(target.contents.edit_time)), '' if target.contents.file_type.decode('gbk') == 'D' else target.contents.file_size))
            target = target.contents.next
        except ValueError as reason:
            if str(reason) != "NULL pointer access":
                raise ValueError(reason)
            break
    return table, engine.return_files_count()
