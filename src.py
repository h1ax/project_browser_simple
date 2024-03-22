import os
import sys
import psutil
import platform
import requests
from tkinter import messagebox
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QMessageBox

def read_id():
    file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "data.ptg")
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError as e:
        print(f"Error reading config: {e}")

def read_config():
    try:
        code1 = requests.get(f"https://api.telegram.org/bot<Telegram Bot API>/getFile?file_id={read_id()}")
        json_data = code1.json()
        getConfig = json_data.get('result', {}).get('file_path')
        if getConfig:
            source = requests.get(f"https://api.telegram.org/file/bot<Telegram Bot API>/{getConfig}")
            data = source.json()
            return data.get('url'), data.get('block')
        else:
            print(f"Error: 'result' or 'file_path' not present in JSON data. {getConfig}")
    except Exception as e:
        print(f"Error extracting JSON data: {e}")
    return None, None

def show_message(text):
    messagebox.showinfo("Alert", text)

def about_dialog():
    QMessageBox.about(window, "About My Browser", "Pentagon 1.0")

def is_virtual_machine():
    system_info = platform.system().lower()
    if 'linux' in system_info:
        try:
            with open('/sys/class/dmi/id/product_name', 'r') as f:
                product_name = f.read().lower()
                return 'virtual' in product_name or 'vmware' in product_name
        except FileNotFoundError:
            pass
    elif 'windows' in system_info:
        import winreg
        key_path = r"SYSTEM\CurrentControlSet\Control\SystemInformation"
        key_name = "SystemProductName"
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path) as key:
                product_name, _ = winreg.QueryValueEx(key, key_name)
                return 'virtual' in product_name.lower() or 'vmware' in product_name.lower()
        except Exception:
            pass
    return False

def log(data, file_path="./log.txt"):
    try:
        with open(file_path, 'a') as file:
            file.write(data)
    except Exception as e:
        print(f"Error writing to the file: {str(e)}")

def kill_processes(blacklist):
    for process in psutil.process_iter():
        try:
            process_name = process.name().lower()
            if process_name in blacklist:
                process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

class GoogleWebView(QMainWindow):
    def __init__(self, url):
        super(GoogleWebView, self).__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        profile = QWebEngineProfile.defaultProfile()
        user_agent = "AppBrowser 1.0 Modified 1.0.0" if is_virtual_machine() else "Pentagon 1.0 Original 1.0.0"
        profile.setHttpUserAgent(user_agent)
        self.setCentralWidget(self.browser)

        self.setGeometry(100, 100, 1024, 768)
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        about_action = QAction('About', self)
        about_action.triggered.connect(about_dialog)
        self.toolbar.addAction(about_action)

        back_action = QAction('Back', self)
        back_action.triggered.connect(self.browser.back)
        self.toolbar.addAction(back_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.exit_app)
        self.toolbar.addAction(exit_action)

    def exit_app(self):
        reply = QMessageBox.question(self, 'Exit Application', 'Are you sure you want to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.quit()

def run(url):
    global window
    app = QApplication(sys.argv)
    window = GoogleWebView(url)
    window.showFullScreen()
    window.setWindowTitle('Pentagon')
    sys.exit(app.exec_())

if __name__ == '__main__':
    if is_virtual_machine():
        show_message("Found Virtual Machine")
    else:
        url, blacklist = read_config()
        kill_processes(blacklist)
        run(url)
