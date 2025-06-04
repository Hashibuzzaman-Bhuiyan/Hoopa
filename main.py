from multiprocessing import Process
import os

def run_hoopa():
    os.system("python3 hoopa.py")

def run_expression():
    os.system("python3 expression.py")

def run_stream():
    os.system("python3 stream.py")

def run_initial():
    os.system("python3 initial.py")

if __name__ == "__main__":
    Process(target=run_hoopa).start()
    Process(target=run_expression).start()
    Process(target=run_stream).start()
    Process(target=run_initial).start()


