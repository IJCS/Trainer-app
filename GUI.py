import tkinter as tk
from tkinter import ttk
import Lang
import Routine

gui_widgets = {}
gui_variables = {}

def setup_window(root):
    root.geometry("400x650")
    root.resizable(False, False)
    center_window(root)

def center_window(root):
    root.update_idletasks()
    width = 400
    height = 650
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

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

def load_config(config_module):
    lang = config_module.General("lang")
    gui_variables["lang"].set("English" if lang == "en" else "Español")
    Lang.set_language(lang)
    
    exelis = config_module.Profile("exelis")
    # Convertir la lista guardada a string simple
    if isinstance(exelis, str):
        # Si viene como "['a', 'b', 'c']", limpiarlo
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

def create_widgets(root, config_module, audio_module):
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    lang_frame = ttk.Frame(main_frame)
    lang_frame.pack(fill=tk.X, pady=(0, 10))
    
    gui_widgets["lang_label"] = ttk.Label(lang_frame, text="Idioma:")
    gui_widgets["lang_label"].pack(side=tk.LEFT, padx=(0, 5))
    lang_combo = ttk.Combobox(lang_frame, textvariable=gui_variables["lang"], 
                              values=["English", "Español"], 
                              state="readonly", width=15)
    lang_combo.pack(side=tk.LEFT)
    lang_combo.bind("<<ComboboxSelected>>", lambda e: on_language_change(config_module, audio_module, root))
    
    gui_widgets["ex_label"] = ttk.Label(main_frame, text="Ejercicios:")
    gui_widgets["ex_label"].pack(anchor=tk.W, pady=(5, 2))
    ttk.Entry(main_frame, textvariable=gui_variables["exelis"]).pack(fill=tk.X, pady=(0, 10))
    
    
    times_frame = ttk.Frame(main_frame)
    times_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Ciclo
    cycle_frame = ttk.Frame(times_frame)
    cycle_frame.pack(fill=tk.X, pady=(0, 5))
    gui_widgets["cycle_label"] = ttk.Label(cycle_frame, text="Ciclo (s):", width=20)
    gui_widgets["cycle_label"].pack(side=tk.LEFT)
    ttk.Spinbox(cycle_frame, from_=1, to=300, textvariable=gui_variables["cyclet"], width=10).pack(side=tk.LEFT)
    
    # Reducción mínima
    minrt_frame = ttk.Frame(times_frame)
    minrt_frame.pack(fill=tk.X, pady=(0, 5))
    gui_widgets["minrt_label"] = ttk.Label(minrt_frame, text="Reducción Mínima (ms):", width=20)
    gui_widgets["minrt_label"].pack(side=tk.LEFT)
    ttk.Spinbox(minrt_frame, from_=0, to=1000, textvariable=gui_variables["minrt"], width=10).pack(side=tk.LEFT)
    
    # Reducción máxima
    maxrt_frame = ttk.Frame(times_frame)
    maxrt_frame.pack(fill=tk.X, pady=(0, 5))
    gui_widgets["maxrt_label"] = ttk.Label(maxrt_frame, text="Reducción Máxima (ms):", width=20)
    gui_widgets["maxrt_label"].pack(side=tk.LEFT)
    ttk.Spinbox(maxrt_frame, from_=0, to=1000, textvariable=gui_variables["maxrt"], width=10).pack(side=tk.LEFT)
    
    # Mínimo de ciclos
    cymin_frame = ttk.Frame(times_frame)
    cymin_frame.pack(fill=tk.X, pady=(0, 5))
    gui_widgets["cymin_label"] = ttk.Label(cymin_frame, text="Mínimo de Ciclos (ms):", width=20)
    gui_widgets["cymin_label"].pack(side=tk.LEFT)
    ttk.Spinbox(cymin_frame, from_=100, to=60000, textvariable=gui_variables["cymin"], width=10).pack(side=tk.LEFT)
    
    gui_widgets["mode_frame"] = ttk.LabelFrame(main_frame, text="Modo", padding="10")
    gui_widgets["mode_frame"].pack(fill=tk.X, pady=(0, 10))
    
    gui_widgets["radio_standard"] = ttk.Radiobutton(gui_widgets["mode_frame"], text="Estándar", 
                                          variable=gui_variables["mode"], value=0, 
                                          command=on_mode_change)
    gui_widgets["radio_standard"].pack(anchor=tk.W)
    
    gui_widgets["radio_series"] = ttk.Radiobutton(gui_widgets["mode_frame"], text="Series", 
                                       variable=gui_variables["mode"], value=1, 
                                       command=on_mode_change)
    gui_widgets["radio_series"].pack(anchor=tk.W)
    
    gui_widgets["radio_cumulative"] = ttk.Radiobutton(gui_widgets["mode_frame"], text="Acumulativo", 
                                           variable=gui_variables["mode"], value=2, 
                                           command=on_mode_change)
    gui_widgets["radio_cumulative"].pack(anchor=tk.W)
    
    gui_widgets["advanced_frame"] = ttk.LabelFrame(main_frame, text="Avanzado", padding="10")
    gui_widgets["advanced_frame"].pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    gui_widgets["series_frame"] = ttk.Frame(gui_widgets["advanced_frame"])
    gui_widgets["cumulative_frame"] = ttk.Frame(gui_widgets["advanced_frame"])
    
    gui_widgets["serre_check"] = ttk.Checkbutton(gui_widgets["series_frame"], text="Permitir repeticiones", 
                                      variable=gui_variables["serre"])
    gui_widgets["serre_check"].pack(anchor=tk.W, pady=(0, 10))
    
    gui_widgets["serin_label"] = ttk.Label(gui_widgets["series_frame"], text="Aumentar:")
    gui_widgets["serin_label"].pack(anchor=tk.W)
    gui_widgets["serin_scale"] = ttk.Scale(gui_widgets["series_frame"], from_=0, to=100, 
                                variable=gui_variables["serin"], orient=tk.HORIZONTAL)
    gui_widgets["serin_scale"].pack(fill=tk.X, pady=(0, 5))
    gui_widgets["serin_value"] = ttk.Label(gui_widgets["series_frame"], text="100")
    gui_widgets["serin_value"].pack(anchor=tk.E)
    gui_widgets["serin_scale"].config(command=lambda v: gui_widgets["serin_value"].config(text=f"{int(float(v))}"))
    
    gui_widgets["serde_label"] = ttk.Label(gui_widgets["series_frame"], text="Disminuir:")
    gui_widgets["serde_label"].pack(anchor=tk.W, pady=(10, 0))
    gui_widgets["serde_scale"] = ttk.Scale(gui_widgets["series_frame"], from_=0, to=100, 
                                variable=gui_variables["serde"], orient=tk.HORIZONTAL)
    gui_widgets["serde_scale"].pack(fill=tk.X, pady=(0, 5))
    gui_widgets["serde_value"] = ttk.Label(gui_widgets["series_frame"], text="0")
    gui_widgets["serde_value"].pack(anchor=tk.E)
    gui_widgets["serde_scale"].config(command=lambda v: gui_widgets["serde_value"].config(text=f"{int(float(v))}"))
    
    gui_widgets["cumre_check"] = ttk.Checkbutton(gui_widgets["cumulative_frame"], text="Permitir repeticiones", 
                                      variable=gui_variables["cumre"])
    gui_widgets["cumre_check"].pack(anchor=tk.W)
    
    status_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
    status_frame.pack(fill=tk.X, pady=(0, 10))
    
    gui_widgets["status_label"] = ttk.Label(status_frame, text="Listo", font=("", 10, "bold"))
    gui_widgets["status_label"].pack(anchor=tk.W)
    
    gui_widgets["time_label"] = ttk.Label(status_frame, text="--")
    gui_widgets["time_label"].pack(anchor=tk.W)
    
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X)
    
    gui_widgets["start_button"] = ttk.Button(button_frame, text="Comenzar", 
                                             command=lambda: toggle_routine(audio_module, root))
    gui_widgets["start_button"].pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)
    
    gui_widgets["save_button"] = ttk.Button(button_frame, text="Guardar", 
                                            command=lambda: save_config(config_module))
    gui_widgets["save_button"].pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    on_mode_change()

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
    gui_widgets["mode_frame"].config(text=Lang.get_text("mode_selection"))
    gui_widgets["radio_standard"].config(text=Lang.get_text("standard"))
    gui_widgets["radio_series"].config(text=Lang.get_text("series"))
    gui_widgets["radio_cumulative"].config(text=Lang.get_text("cumulative"))
    gui_widgets["advanced_frame"].config(text=Lang.get_text("advanced_actions"))
    gui_widgets["serre_check"].config(text=Lang.get_text("allow_repetitions"))
    gui_widgets["cumre_check"].config(text=Lang.get_text("allow_repetitions"))
    gui_widgets["serin_label"].config(text=Lang.get_text("increase_probability"))
    gui_widgets["serde_label"].config(text=Lang.get_text("decrease_probability"))
    gui_widgets["save_button"].config(text=Lang.get_text("save_config"))
    
    if Routine.is_running():
        gui_widgets["start_button"].config(text=Lang.get_text("stop"))
    else:
        gui_widgets["start_button"].config(text=Lang.get_text("start"))

def on_mode_change():
    gui_widgets["series_frame"].pack_forget()
    gui_widgets["cumulative_frame"].pack_forget()
    
    mode = gui_variables["mode"].get()
    if mode == 0:
        gui_widgets["advanced_frame"].pack_forget()
    elif mode == 1:
        gui_widgets["advanced_frame"].pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        gui_widgets["series_frame"].pack(fill=tk.BOTH, expand=True)
    elif mode == 2:
        gui_widgets["advanced_frame"].pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        gui_widgets["cumulative_frame"].pack(fill=tk.BOTH, expand=True)

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

def toggle_routine(audio_module, root):
    if Routine.is_running():
        Routine.stop_routine()
        gui_widgets["start_button"].config(text=Lang.get_text("start"))
        gui_widgets["status_label"].config(text=Lang.get_text("status_idle"))
        gui_widgets["time_label"].config(text="--")
    else:
        exercises = [x.strip() for x in gui_variables["exelis"].get().split(",")]
        Routine.configure_routine(
            exercises, gui_variables["cyclet"].get(), gui_variables["minrt"].get(),
            gui_variables["maxrt"].get(), gui_variables["cymin"].get() / 1000,  # Convertir ms a segundos
            gui_variables["mode"].get(),
            gui_variables["serre"].get(), gui_variables["serin"].get(), gui_variables["serde"].get(),
            gui_variables["cumre"].get()
        )
        Routine.set_status_callback(lambda s, e, el, r: update_status(root, s, e, el, r))
        Routine.start_routine(audio_module)
        gui_widgets["start_button"].config(text=Lang.get_text("stop"))

def update_status(root, status, exercise, elapsed, remaining):
    if status == "preparing":
        text = Lang.get_text("status_preparing")
    elif status == "running":
        if isinstance(exercise, list):
            exercise_text = " → ".join(exercise)
        else:
            exercise_text = exercise
        text = Lang.get_text("status_running").format(exercise=exercise_text)
        time_text = Lang.get_text("time_info").format(
            elapsed=int(elapsed), 
            remaining=int(remaining)
        )
        root.after(0, lambda: gui_widgets["time_label"].config(text=time_text))
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