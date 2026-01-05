import tkinter as tk
import Config
import Audio
import GUI

if __name__ == "__main__":
    root = tk.Tk()
    GUI.init_gui(root, Config, Audio)
    root.mainloop()