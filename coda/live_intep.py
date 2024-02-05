import json
from tojson import codaToJson

import os,sys
os.system("CLS")
print("Simple Coda Interpriter (v1.0, by: Simon Kalmi Claesson) [Coda_M.I_Set]")
print("Write 'help' for help.")
while True:
    try:
        c = input("Coda> ")
    except KeyboardInterrupt:
        exit()
    if "--i" in sys.argv:
        i = 2
    else:
        i = None
    if "--d" in sys.argv:
        _deb_codaToJson = True
    else:
        _deb_codaToJson = False
    if c[0] == "!":
        i = 2
    if ";" in c:
        c = c.split(";")
    else:
        c = [c]
    _dict = {}
    toExec = []
    for p in c:
        if p == "exit":
            exit()
        elif p == "cls":
            os.system("CLS")
        elif p == "help":
            print("  'cls': Clears screen.\n  'exit': Exits.\n  'help': Shows this info.\n  Commands are comma sepparated.")
        else:
            toExec.append(p)
    _dict.update(codaToJson('\n'.join(toExec),True,_dict,debug=_deb_codaToJson))
    if _dict != {}:
        print(json.dumps(_dict,indent=i))