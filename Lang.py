TEXTS = {
    "en": {
        "title": "Trainer-app",
        "language": "Language:",
        "exercises": "Exercises List (comma separated):",
        "cycle_time": "Cycle:",
        "min_reduction": "Reduction Minimum:",
        "max_reduction": "Reduction Maximum:",
        "min_cycle": "Cycle Minimum:",
        "voice_speed": "Voice speed:",
        "word_spacing": "Word spacing:",
        "mode_selection": "Mode Selection",
        "standard": "Standard",
        "series": "Series",
        "cumulative": "Cumulative",
        "advanced_actions": "Advanced Actions",
        "wait_narrator": "Wait for narrator",
        "allow_repetitions": "Allow repetitions",
        "increase_probability": "Increase probability:",
        "decrease_probability": "Decrease probability:",
        "start": "Start",
        "stop": "Stop",
        "status_idle": "Ready to start",
        "status_preparing": "Preparing routine...",
        "status_running": "Running: {exercise}",
        "time_info": "Elapsed: {elapsed}s | Next: {remaining}s",
        "save_config": "Save Configuration",
        "config_saved": "configuration saved",
        "starting_routine": "starting routine",
        "cycle_help": "Duration of each exercise cycle in seconds.",
        "minrt_help": "Minimum random reduction value for cycle duration in milliseconds.",
        "maxrt_help": "Maximum random reduction value for cycle duration in milliseconds.",
        "cymin_help": "Minimum value that cycle duration can reach in milliseconds."
    },
    "es": {
        "title": "Trainer-app",
        "language": "Idioma:",
        "exercises": "Lista de Ejercicios (separados por comas):",
        "cycle_time": "Ciclo:",
        "min_reduction": "Reducción Mínima:",
        "max_reduction": "Reducción Máxima:",
        "min_cycle": "Mínimo de Ciclos:",
        "voice_speed": "Velocidad de voz:",
        "word_spacing": "Espacio entre palabras:",
        "mode_selection": "Selección de Modo",
        "standard": "Estándar",
        "series": "Series",
        "cumulative": "Acumulativo",
        "advanced_actions": "Acciones Avanzadas",
        "wait_narrator": "Esperar al narrador",
        "allow_repetitions": "Permitir repeticiones",
        "increase_probability": "Probabilidad de aumentar:",
        "decrease_probability": "Probabilidad de disminuir:",
        "start": "Comenzar",
        "stop": "Detener",
        "status_idle": "Listo para comenzar",
        "status_preparing": "Preparando rutina...",
        "status_running": "Ejecutando: {exercise}",
        "time_info": "Transcurrido: {elapsed}s | Próximo: {remaining}s",
        "save_config": "Guardar Configuración",
        "config_saved": "configuración guardada",
        "starting_routine": "iniciando rutina",
        "cycle_help": "Duración de cada ciclo de ejercicios en segundos.",
        "minrt_help": "Valor mínimo de reducción aleatoria de duración entre ciclos en milisegundos.",
        "maxrt_help": "Valor máximo de reducción aleatoria de duración entre ciclos en milisegundos.",
        "cymin_help": "Valor mínimo al que puede llegar la duración del ciclo en milisegundos."
    }
}

current_language = "en"

def set_language(lang):
    global current_language
    current_language = lang

def get_text(key):
    return TEXTS.get(current_language, TEXTS["en"]).get(key, key)