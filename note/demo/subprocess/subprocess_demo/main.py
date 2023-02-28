import logging
import os
import subprocess
import sys

from kivy.uix.button import Button
from kivy.base import runTouchApp, stopTouchApp

if "StartFromUpdate" not in sys.argv:
    logging.info("start updater")
    if getattr(sys, 'frozen', False):
        updater = os.path.join(os.getcwd(), "update.exe")
    else:
        updater = os.path.join(os.getcwd(), "dist/update/update.exe")
    subprocess.Popen([updater], shell=False, stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE, stdin=subprocess.PIPE)
else:
    logging.info("StartFromUpdate")

logging.info("start main app")
runTouchApp(Button(text="this main process",  on_release=lambda *args: stopTouchApp()))
logging.info("start main exit")
