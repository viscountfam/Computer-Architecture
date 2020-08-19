#!/usr/bin/env python3

"""Main."""
from os import listdir
import sys
from cpu import *


cpu = CPU()

# cpu.load()
# cpu.run()

files = {file for file in listdir("examples")}

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    if file_name in files:
        cpu.load(file_name)
    else:
        print("An invalid file was selected")
        sys.exit()
else:
    cpu.load("print8.ls8")
cpu.run()