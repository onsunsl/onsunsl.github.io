import os
from time import sleep
import signal
import sys
from traceback import extract_stack


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    f = open("./1.txt", "w")
    f.write("sigterm_handler")
    f.close()
    sys.exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)

try:
    print(os.getpid(), os.getppid())
    print("Hello")
    i = 0
    while True:
        i += 1
        print("Iteration #%i" % i)
        sleep(1)
finally:
    print("Goodbye")