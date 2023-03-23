import subprocess

def exchange():
    subprocess.run("./START.exe")

def getResult():
    with open("Results.txt", "r") as f:
        text = f.read()
        return text