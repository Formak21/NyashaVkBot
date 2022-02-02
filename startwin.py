from subprocess import Popen

while True:
    print("\nStarted.")
    p = Popen("python remain.py", shell=True)
    p.wait()
