from subprocess import Popen

while True:
    print("\nStarted.")
    p = Popen("python3 remain.py", shell=True)
    p.wait()
