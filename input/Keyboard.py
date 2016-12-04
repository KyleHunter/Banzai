import win32com.client
from time import sleep


def type_key(key):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys(key)


def type_send(key):
    type_key(key)
    sleep(0.05)
    type_key("{enter}")
