import logging
from kivy.uix.button import Button
from kivy.base import runTouchApp, stopTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import subprocess


class Updater(BoxLayout):
    main_process: subprocess.Popen = None

    def __init__(self, **kwargs):
        super(Updater, self).__init__(**kwargs)
        self.text = TextInput()
        self.add_widget(self.text)
        self.button = Button(text="check", on_release=self.on_check)
        self.add_widget(self.button)

    def on_check(self, inc, *args):
        if self.text.text == "1":
            cmd = ["main.exe", "StartFromUpdate"]
            subprocess.run("taskkill /f /pid main.exe".split(" "))
            Updater.main_process = subprocess.Popen(cmd, shell=False, stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            stopTouchApp()


logging.info("start updater..")
runTouchApp(Updater())

logging.info("waite main exit")
Updater.main_process.wait()

logging.info("updater exit")

        
