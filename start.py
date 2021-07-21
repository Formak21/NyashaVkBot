from subprocess import Popen
import sys

filename = 'main.py'
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()