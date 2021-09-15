from subprocess import Popen

while True:
    print("\nStarted.")
    p = Popen("python main.py", shell=True)
    p.wait()