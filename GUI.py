import tkinter as tk
from tkinter import ttk
import sys
import Lang
import Routine
import os

gui_widgets = {}
gui_variables = {}
advanced_window = None

def recurse(rute):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rute)

def setup_window(root):
    icon = tk.PhotoImage(file=recurse('Icon.png'))
    root.iconphoto(True, icon)
    root.geometry("400x680")
    root.resizable(False, False)
    center_window(root)

def center_window(root):
    root.update_idletasks()
    width = 400
    height = 720
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=("tahoma", "8", "normal"), wraplength=250)
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def create_variables():
    gui_variables["lang"] = tk.StringVar()
    gui_variables["exelis"] = tk.StringVar()
    gui_variables["cyclet"] = tk.IntVar()
    gui_variables["minrt"] = tk.IntVar()
    gui_variables["maxrt"] = tk.IntVar()
    gui_variables["cymin"] = tk.IntVar()
    gui_variables["mode"] = tk.IntVar()
    gui_variables["serre"] = tk.BooleanVar()
    gui_variables["serin"] = tk.IntVar()
    gui_variables["serde"] = tk.IntVar()
    gui_variables["cumre"] = tk.BooleanVar()
    gui_variables["rate"] = tk.IntVar()
    gui_variables["pause"] = tk.IntVar()
    gui_variables["waitnar"] = tk.BooleanVar()

def load_config(config_module):
    lang = config_module.General("lang")
    gui_variables["lang"].set("English" if lang == "en" else "Español")
    Lang.set_language(lang)
    
    exelis = config_module.Profile("exelis")
    if isinstance(exelis, str):
        if exelis.startswith('[') and exelis.endswith(']'):
            exelis = exelis.strip('[]').replace("'", "").replace('"', '')
        gui_variables["exelis"].set(exelis)
    else:
        gui_variables["exelis"].set(", ".join(map(str, exelis)))
    
    gui_variables["cyclet"].set(config_module.Profile("cyclet"))
    gui_variables["minrt"].set(config_module.Profile("minrt"))
    gui_variables["maxrt"].set(config_module.Profile("maxrt"))
    
    try:
        gui_variables["cymin"].set(config_module.Profile("cymin"))
    except:
        gui_variables["cymin"].set(1000)
    
    gui_variables["mode"].set(config_module.Profile("mode"))
    gui_variables["serre"].set(config_module.Advanced("serre"))
    gui_variables["serin"].set(config_module.Advanced("serin"))
    gui_variables["serde"].set(config_module.Advanced("serde"))
    gui_variables["cumre"].set(config_module.Advanced("cumre"))
    
    try:
        gui_variables["waitnar"].set(config_module.Advanced("waitnar"))
    except:
        gui_variables["waitnar"].set(True)
    
    try:
        gui_variables["rate"].set(config_module.Audio("rate"))
        gui_variables["pause"].set(config_module.Audio("pause"))
    except:
        gui_variables["rate"].set(150)
        gui_variables["pause"].set(500)

def show_about_window(root):
    about = tk.Toplevel(root)
    about.title("About")
    about.geometry("300x480")
    about.resizable(False, False)
    
    about.update_idletasks()
    x = (about.winfo_screenwidth() // 2) - (300 // 2)
    y = (about.winfo_screenheight() // 2) - (480 // 2)
    about.geometry(f'300x480+{x}+{y}')
    
    frame = ttk.Frame(about, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    try:
        icon_img = tk.PhotoImage(file=recurse('Icon.png'))
        icon_label = ttk.Label(frame, image=icon_img)
        icon_label.image = icon_img
        icon_label.pack(pady=(0, 10))
    except:
        pass
    
    ttk.Label(frame, text="Trainer-app", font=("", 14, "bold")).pack(pady=(0, 5))
    ttk.Label(frame, text="IJCS - 2026").pack(pady=(0, 15))
    
    github_frame = ttk.Frame(frame)
    github_frame.pack(pady=5)
    ttk.Label(github_frame, text="GitHub: ").pack(side=tk.LEFT)
    github_link = ttk.Label(github_frame, text="github.com/IJCS/Trainer-app", 
                           foreground="blue", cursor="hand2")
    github_link.pack(side=tk.LEFT)
    github_link.bind("<Button-1>", lambda e: open_url("https://github.com/IJCS/Trainer-app"))
    
    kofi_frame = ttk.Frame(frame)
    kofi_frame.pack(pady=5)
    ttk.Label(kofi_frame, text="Support: ").pack(side=tk.LEFT)
    kofi_link = ttk.Label(kofi_frame, text="ko-fi.com/H2H11RMG69", 
                         foreground="blue", cursor="hand2")
    kofi_link.pack(side=tk.LEFT)
    kofi_link.bind("<Button-1>", lambda e: open_url("https://ko-fi.com/H2H11RMG69"))

def open_url(url):
    import webbrowser
    webbrowser.open(url)

def show_advanced_window(root, config_module):
    global advanced_window
    
    if advanced_window and advanced_window.winfo_exists():
        advanced_window.lift()
        return
    
    advanced_window = tk.Toplevel(root)
    advanced_window.title(Lang.get_text("advanced_actions"))
    advanced_window.geometry("350x400")
    advanced_window.resizable(False, False)
    
    advanced_window.update_idletasks()
    x = (advanced_window.winfo_screenwidth() // 2) - (350 // 2)
    y = (advanced_window.winfo_screenheight() // 2) - (400 // 2)
    advanced_window.geometry(f'350x400+{x}+{y}')
    
    gui_widgets["advanced_button"].config(state="disabled")
    
    def on_close():
        global advanced_window
        gui_widgets["advanced_button"].config(state="normal")
        save_config(config_module)
        advanced_window.destroy()
        advanced_window = None
    
    advanced_window.protocol("WM_DELETE_WINDOW", on_close)
    
    main_frame = ttk.Frame(advanced_window, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    mode = gui_variables["mode"].get()
    
    if mode == 0:
        ttk.Checkbutton(main_frame, text=Lang.get_text("wait_narrator"), 
                       variable=gui_variables["waitnar"]).pack(anchor=tk.W, pady=10)
    
    elif mode == 1:
        ttk.Checkbutton(main_frame, text=Lang.get_text("allow_repetitions"), 
                       variable=gui_variables["serre"]).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text=Lang.get_text("increase_probability")).pack(anchor=tk.W)
        serin_scale = ttk.Scale(main_frame, from_=0, to=100, 
                               variable=gui_variables["serin"], orient=tk.HORIZONTAL)
        serin_scale.pack(fill=tk.X, pady=(0, 5))
        serin_value = ttk.Label(main_frame, text=str(gui_variables["serin"].get()))
        serin_value.pack(anchor=tk.E)
        
        ttk.Label(main_frame, text=Lang.get_text("decrease_probability")).pack(anchor=tk.W, pady=(10, 0))
        serde_scale = ttk.Scale(main_frame, from_=0, to=100, 
                               variable=gui_variables["serde"], orient=tk.HORIZONTAL)
        serde_scale.pack(fill=tk.X, pady=(0, 5))
        serde_value = ttk.Label(main_frame, text=str(gui_variables["serde"].get()))
        serde_value.pack(anchor=tk.E)
        
        def update_serin_adv(v):
            serin_val = int(float(v))
            serin_value.config(text=f"{serin_val}")
            max_serde = 100 - serin_val
            serde_scale.config(to=max_serde)
            if gui_variables["serde"].get() > max_serde:
                gui_variables["serde"].set(max_serde)
                serde_value.config(text=f"{max_serde}")
        
        def update_serde_adv(v):
            serde_val = int(float(v))
            serde_value.config(text=f"{serde_val}")
        
        serin_scale.config(command=update_serin_adv)
        serde_scale.config(command=update_serde_adv)
        
        update_serin_adv(gui_variables["serin"].get())
    
    elif mode == 2:
        ttk.Checkbutton(main_frame, text=Lang.get_text("allow_repetitions"), 
                       variable=gui_variables["cumre"]).pack(anchor=tk.W, pady=10)

def create_widgets(root, config_module, audio_module):
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 10))
    
    lang_left = ttk.Frame(header_frame)
    lang_left.pack(side=tk.LEFT)
    
    gui_widgets["lang_label"] = ttk.Label(lang_left, text="Idioma:")
    gui_widgets["lang_label"].pack(side=tk.LEFT, padx=(0, 5))
    lang_combo = ttk.Combobox(lang_left, textvariable=gui_variables["lang"], 
                              values=["English", "Español"], 
                              state="readonly", width=15)
    lang_combo.pack(side=tk.LEFT)
    lang_combo.bind("<<ComboboxSelected>>", lambda e: on_language_change(config_module, audio_module, root))
    
    about_button = ttk.Button(header_frame, text="?", width=3, 
                             command=lambda: show_about_window(root))
    about_button.pack(side=tk.RIGHT)
    
    gui_widgets["ex_label"] = ttk.Label(main_frame, text="Ejercicios:")
    gui_widgets["ex_label"].pack(anchor=tk.W, pady=(5, 2))
    ttk.Entry(main_frame, textvariable=gui_variables["exelis"]).pack(fill=tk.X, pady=(0, 10))
    
    times_frame = ttk.Frame(main_frame)
    times_frame.pack(fill=tk.X, pady=(0, 10))
    
    cycle_frame = ttk.Frame(times_frame)
    cycle_frame.pack(fill=tk.X, pady=(0, 5))
    
    cycle_label_frame = ttk.Frame(cycle_frame)
    cycle_label_frame.pack(side=tk.LEFT)
    gui_widgets["cycle_label"] = ttk.Label(cycle_label_frame, text="Ciclo:")
    gui_widgets["cycle_label"].pack(side=tk.LEFT)
    cycle_help = ttk.Label(cycle_label_frame, text="(?)", foreground="blue", cursor="hand2")
    cycle_help.pack(side=tk.LEFT, padx=(2, 0))
    ToolTip(cycle_help, Lang.get_text("cycle_help"))
    
    cycle_spin = ttk.Spinbox(cycle_frame, from_=1, to=300, textvariable=gui_variables["cyclet"], width=8)
    cycle_spin.pack(side=tk.RIGHT, padx=(5, 0))
    gui_widgets["cycle_unit"] = ttk.Label(cycle_frame, text="s")
    gui_widgets["cycle_unit"].pack(side=tk.RIGHT)
    
    minrt_frame = ttk.Frame(times_frame)
    minrt_frame.pack(fill=tk.X, pady=(0, 5))
    
    minrt_label_frame = ttk.Frame(minrt_frame)
    minrt_label_frame.pack(side=tk.LEFT)
    gui_widgets["minrt_label"] = ttk.Label(minrt_label_frame, text="Reducción Mínima:")
    gui_widgets["minrt_label"].pack(side=tk.LEFT)
    minrt_help = ttk.Label(minrt_label_frame, text="(?)", foreground="blue", cursor="hand2")
    minrt_help.pack(side=tk.LEFT, padx=(2, 0))
    ToolTip(minrt_help, Lang.get_text("minrt_help"))
    
    def validate_minrt(*args):
        if gui_variables["minrt"].get() > gui_variables["maxrt"].get():
            gui_variables["minrt"].set(gui_variables["maxrt"].get())
    
    gui_variables["minrt"].trace_add("write", validate_minrt)
    gui_variables["maxrt"].trace_add("write", validate_minrt)
    
    minrt_spin = ttk.Spinbox(minrt_frame, from_=0, to=1000, textvariable=gui_variables["minrt"], width=8)
    minrt_spin.pack(side=tk.RIGHT, padx=(5, 0))
    gui_widgets["minrt_unit"] = ttk.Label(minrt_frame, text="ms")
    gui_widgets["minrt_unit"].pack(side=tk.RIGHT)
    
    maxrt_frame = ttk.Frame(times_frame)
    maxrt_frame.pack(fill=tk.X, pady=(0, 5))
    
    maxrt_label_frame = ttk.Frame(maxrt_frame)
    maxrt_label_frame.pack(side=tk.LEFT)
    gui_widgets["maxrt_label"] = ttk.Label(maxrt_label_frame, text="Reducción Máxima:")
    gui_widgets["maxrt_label"].pack(side=tk.LEFT)
    maxrt_help = ttk.Label(maxrt_label_frame, text="(?)", foreground="blue", cursor="hand2")
    maxrt_help.pack(side=tk.LEFT, padx=(2, 0))
    ToolTip(maxrt_help, Lang.get_text("maxrt_help"))
    
    maxrt_spin = ttk.Spinbox(maxrt_frame, from_=0, to=1000, textvariable=gui_variables["maxrt"], width=8)
    maxrt_spin.pack(side=tk.RIGHT, padx=(5, 0))
    gui_widgets["maxrt_unit"] = ttk.Label(maxrt_frame, text="ms")
    gui_widgets["maxrt_unit"].pack(side=tk.RIGHT)
    
    cymin_frame = ttk.Frame(times_frame)
    cymin_frame.pack(fill=tk.X, pady=(0, 5))
    
    cymin_label_frame = ttk.Frame(cymin_frame)
    cymin_label_frame.pack(side=tk.LEFT)
    gui_widgets["cymin_label"] = ttk.Label(cymin_label_frame, text="Mínimo de Ciclos:")
    gui_widgets["cymin_label"].pack(side=tk.LEFT)
    cymin_help = ttk.Label(cymin_label_frame, text="(?)", foreground="blue", cursor="hand2")
    cymin_help.pack(side=tk.LEFT, padx=(2, 0))
    ToolTip(cymin_help, Lang.get_text("cymin_help"))
    
    cymin_spin = ttk.Spinbox(cymin_frame, from_=0, to=60000, textvariable=gui_variables["cymin"], 
                            width=8)
    cymin_spin.pack(side=tk.RIGHT, padx=(5, 0))
    gui_widgets["cymin_unit"] = ttk.Label(cymin_frame, text="ms")
    gui_widgets["cymin_unit"].pack(side=tk.RIGHT)
    
    audio_frame = ttk.LabelFrame(main_frame, text="Audio", padding="10")
    audio_frame.pack(fill=tk.X, pady=(0, 10))
    
    rate_frame = ttk.Frame(audio_frame)
    rate_frame.pack(fill=tk.X, pady=(0, 5))
    gui_widgets["rate_label"] = ttk.Label(rate_frame, text="Velocidad de voz:")
    gui_widgets["rate_label"].pack(anchor=tk.W)
    gui_widgets["rate_scale"] = ttk.Scale(rate_frame, from_=50, to=300, 
                                variable=gui_variables["rate"], orient=tk.HORIZONTAL)
    gui_widgets["rate_scale"].pack(fill=tk.X, pady=(0, 2))
    gui_widgets["rate_value"] = ttk.Label(rate_frame, text=f"{gui_variables['rate'].get()}")
    gui_widgets["rate_value"].pack(anchor=tk.E)
    gui_widgets["rate_scale"].config(command=lambda v: update_rate_label(v, audio_module))
    
    pause_frame = ttk.Frame(audio_frame)
    pause_frame.pack(fill=tk.X)
    gui_widgets["pause_label"] = ttk.Label(pause_frame, text="Espacio entre palabras:")
    gui_widgets["pause_label"].pack(anchor=tk.W)
    gui_widgets["pause_scale"] = ttk.Scale(pause_frame, from_=0, to=2000, 
                                variable=gui_variables["pause"], orient=tk.HORIZONTAL)
    gui_widgets["pause_scale"].pack(fill=tk.X, pady=(0, 2))
    gui_widgets["pause_value"] = ttk.Label(pause_frame, text=f"{gui_variables['pause'].get()} ms")
    gui_widgets["pause_value"].pack(anchor=tk.E)
    gui_widgets["pause_scale"].config(command=lambda v: update_pause_label(v, audio_module))
    
    gui_widgets["mode_frame"] = ttk.LabelFrame(main_frame, text="Modo", padding="10")
    gui_widgets["mode_frame"].pack(fill=tk.X, pady=(0, 10))
    
    gui_widgets["radio_standard"] = ttk.Radiobutton(gui_widgets["mode_frame"], text="Estándar", 
                                          variable=gui_variables["mode"], value=0,
                                          command=lambda: on_mode_change(config_module))
    gui_widgets["radio_standard"].pack(anchor=tk.W)
    
    gui_widgets["radio_series"] = ttk.Radiobutton(gui_widgets["mode_frame"], text="Series", 
                                       variable=gui_variables["mode"], value=1,
                                       command=lambda: on_mode_change(config_module))
    gui_widgets["radio_series"].pack(anchor=tk.W)
    
    gui_widgets["radio_cumulative"] = ttk.Radiobutton(gui_widgets["mode_frame"], text="Acumulativo", 
                                           variable=gui_variables["mode"], value=2,
                                           command=lambda: on_mode_change(config_module))
    gui_widgets["radio_cumulative"].pack(anchor=tk.W)
    
    gui_widgets["advanced_button"] = ttk.Button(main_frame, text=Lang.get_text("advanced_actions"),
                                                command=lambda: show_advanced_window(root, config_module))
    gui_widgets["advanced_button"].pack(fill=tk.X, pady=(0, 10))
    
    status_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
    status_frame.pack(fill=tk.X, pady=(0, 10))
    
    gui_widgets["status_label"] = ttk.Label(status_frame, text="Listo", font=("", 10, "bold"))
    gui_widgets["status_label"].pack(anchor=tk.W)
    
    gui_widgets["cycle_count_label"] = ttk.Label(status_frame, text="Ciclo: 0")
    gui_widgets["cycle_count_label"].pack(anchor=tk.W)
    
    gui_widgets["next_label"] = ttk.Label(status_frame, text="Próximo: -- ms")
    gui_widgets["next_label"].pack(anchor=tk.W)
    
    gui_widgets["session_label"] = ttk.Label(status_frame, text="Sesión: 0 s")
    gui_widgets["session_label"].pack(anchor=tk.W)
    
    gui_widgets["start_button"] = ttk.Button(main_frame, text="Comenzar", 
                                             command=lambda: toggle_routine(audio_module, root, config_module))
    gui_widgets["start_button"].pack(fill=tk.X)
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, config_module))

def on_mode_change(config_module):
    global advanced_window
    if advanced_window and advanced_window.winfo_exists():
        advanced_window.destroy()
        advanced_window = None
        gui_widgets["advanced_button"].config(state="normal")

def on_closing(root, config_module):
    save_config(config_module)
    root.destroy()

def update_rate_label(value, audio_module):
    rate_val = int(float(value))
    gui_widgets["rate_value"].config(text=f"{rate_val}")
    audio_module.set_rate(rate_val)

def update_pause_label(value, audio_module):
    pause_val = int(float(value))
    gui_widgets["pause_value"].config(text=f"{pause_val} ms")
    audio_module.set_pause(pause_val)

def on_language_change(config_module, audio_module, root):
    lang_code = "en" if gui_variables["lang"].get() == "English" else "es"
    Lang.set_language(lang_code)
    config_module.Set("General", "lang", lang_code)
    audio_module.set_language(lang_code)
    update_language(root)

def update_language(root):
    root.title(Lang.get_text("title"))
    gui_widgets["lang_label"].config(text=Lang.get_text("language"))
    gui_widgets["ex_label"].config(text=Lang.get_text("exercises"))
    gui_widgets["cycle_label"].config(text=Lang.get_text("cycle_time"))
    gui_widgets["minrt_label"].config(text=Lang.get_text("min_reduction"))
    gui_widgets["maxrt_label"].config(text=Lang.get_text("max_reduction"))
    gui_widgets["cymin_label"].config(text=Lang.get_text("min_cycle"))
    gui_widgets["rate_label"].config(text=Lang.get_text("voice_speed"))
    gui_widgets["pause_label"].config(text=Lang.get_text("word_spacing"))
    gui_widgets["mode_frame"].config(text=Lang.get_text("mode_selection"))
    gui_widgets["radio_standard"].config(text=Lang.get_text("standard"))
    gui_widgets["radio_series"].config(text=Lang.get_text("series"))
    gui_widgets["radio_cumulative"].config(text=Lang.get_text("cumulative"))
    gui_widgets["advanced_button"].config(text=Lang.get_text("advanced_actions"))
    
    if Routine.is_running():
        gui_widgets["start_button"].config(text=Lang.get_text("stop"))
    else:
        gui_widgets["start_button"].config(text=Lang.get_text("start"))

def save_config(config_module):
    lang_code = "en" if gui_variables["lang"].get() == "English" else "es"
    config_module.Set("General", "lang", lang_code)
    
    exelis_str = gui_variables["exelis"].get()
    config_module.Set("Profile", "exelis", exelis_str)
    config_module.Set("Profile", "cyclet", gui_variables["cyclet"].get())
    config_module.Set("Profile", "minrt", gui_variables["minrt"].get())
    config_module.Set("Profile", "maxrt", gui_variables["maxrt"].get())
    config_module.Set("Profile", "cymin", gui_variables["cymin"].get())
    config_module.Set("Profile", "mode", gui_variables["mode"].get())
    
    config_module.Set("Advanced", "serre", gui_variables["serre"].get())
    config_module.Set("Advanced", "serin", gui_variables["serin"].get())
    config_module.Set("Advanced", "serde", gui_variables["serde"].get())
    config_module.Set("Advanced", "cumre", gui_variables["cumre"].get())
    config_module.Set("Advanced", "waitnar", gui_variables["waitnar"].get())
    
    config_module.Set("Audio", "rate", gui_variables["rate"].get())
    config_module.Set("Audio", "pause", gui_variables["pause"].get())

def toggle_routine(audio_module, root, config_module):
    if Routine.is_running():
        Routine.stop_routine()
        gui_widgets["start_button"].config(text=Lang.get_text("start"))
        gui_widgets["status_label"].config(text=Lang.get_text("status_idle"))
        gui_widgets["cycle_count_label"].config(text="Ciclo: 0")
        gui_widgets["next_label"].config(text="Próximo: -- ms")
        gui_widgets["session_label"].config(text="Sesión: 0 s")
    else:
        save_config(config_module)
        
        exercises = [x.strip() for x in gui_variables["exelis"].get().split(",")]
        Routine.configure_routine(
            exercises, gui_variables["cyclet"].get(), gui_variables["minrt"].get(),
            gui_variables["maxrt"].get(), gui_variables["cymin"].get() / 1000,
            gui_variables["mode"].get(),
            gui_variables["serre"].get(), gui_variables["serin"].get(), gui_variables["serde"].get(),
            gui_variables["cumre"].get(), gui_variables["waitnar"].get()
        )
        Routine.set_status_callback(lambda s, e, c, r, t: update_status(root, s, e, c, r, t))
        Routine.start_routine(audio_module)
        gui_widgets["start_button"].config(text=Lang.get_text("stop"))

def update_status(root, status, exercise, cycle_count, next_duration, total_time):
    if status == "preparing":
        text = Lang.get_text("status_preparing")
        root.after(0, lambda: gui_widgets["cycle_count_label"].config(text="Ciclo: 0"))
        root.after(0, lambda: gui_widgets["next_label"].config(text="Próximo: -- ms"))
        root.after(0, lambda: gui_widgets["session_label"].config(text="Sesión: 0 s"))
    elif status == "running":
        if isinstance(exercise, list):
            exercise_text = " → ".join(exercise)
        else:
            exercise_text = exercise
        text = Lang.get_text("status_running").format(exercise=exercise_text)
        root.after(0, lambda: gui_widgets["cycle_count_label"].config(text=f"Ciclo: {cycle_count}"))
        root.after(0, lambda: gui_widgets["next_label"].config(text=f"Próximo: {int(next_duration * 1000)} ms"))
        root.after(0, lambda: gui_widgets["session_label"].config(text=f"Sesión: {int(total_time)} s"))
    else:
        text = Lang.get_text("status_idle")
    
    root.after(0, lambda: gui_widgets["status_label"].config(text=text))

def init_gui(root, config_module, audio_module):
    setup_window(root)
    create_variables()
    load_config(config_module)
    create_widgets(root, config_module, audio_module)
    update_language(root)
    
    lang_code = "en" if gui_variables["lang"].get() == "English" else "es"
    audio_module.set_language(lang_code)
    audio_module.set_rate(gui_variables["rate"].get())
    audio_module.set_pause(gui_variables["pause"].get())