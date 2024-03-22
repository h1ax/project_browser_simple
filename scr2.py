import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import os
import json
import tempfile

class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x500")  # Kích thước màn hình
        self.master.title("GUI")

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Tab 1
        self.tab1_label = tk.Label(self.frame, text="Enter URL:")
        self.tab1_label.pack(pady=10)

        self.url_entry = tk.Entry(self.frame, width=50)  # Chiều rộng của khung nhập chuỗi
        self.url_entry.pack(pady=10)

        # Tab 2
        self.tab2_label = tk.Label(self.frame, text="Select files:")
        self.tab2_label.pack(pady=10)

        self.browse_button = tk.Button(self.frame, text="Browse", command=self.browse_files)
        self.browse_button.pack(pady=10)

        self.selected_files_listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, width=50)  # Chiều rộng của Listbox
        self.selected_files_listbox.pack(pady=10)

        # Tab 3
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.show_alert)
        self.submit_button.pack(pady=10)

        # Instance variable to store selected files
        self.block = []

    def get_actual_file_name(self, file_path):
        if file_path.lower().endswith('.lnk'):
            with open(file_path, 'r', encoding='utf-16') as shortcut_file:
                lines = shortcut_file.readlines()
                for line in lines:
                    if line.startswith('IconFile='):
                        icon_path = line[len('IconFile='):].strip()
                        return os.path.basename(icon_path)

        return os.path.basename(file_path)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames()
        self.selected_files_listbox.delete(0, tk.END)
        self.block = []
        for file_path in file_paths:
            file_name = self.get_actual_file_name(file_path).lower()
            self.selected_files_listbox.insert(tk.END, file_name)
            self.block.append(file_name)  # Update the instance variable

    def show_alert(self):
        url = self.url_entry.get()
        data = {
            "url": url,
            "block": self.block
        }

        check = send_document(data).json()
        if check:
            messagebox.showinfo("Notice", "done ùi đó\n")
            with open('data.ptg', 'w') as file:
              file.write(check.get('result', {}).get('document').get('file_id'))


def send_document(cf):
    file_data = json.dumps(cf, indent=2).encode('utf-8')
    encoded_data = file_data
    data = {
        'chat_id': 'your chat id',
        'caption': 'config'
    }

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(encoded_data)
        temp_file_path = temp_file.name

    files = {'document': open(temp_file_path, 'rb')}
    response = requests.post(
        'https://api.telegram.org/bot<Telegram Bot API>/sendDocument',
        data=data,
        files=files
    )
    return response

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
