TEXTS = {
    "en": {
        "title": "Trainer-app",
        "language": "Language:",
        "exercises": "Exercises List (comma separated):",
        "cycle_time": "Cycle (s):",
        "min_reduction": "Reduction Minimum (ms):",
        "max_reduction": "Reduction Maximum (ms):",
        "min_cycle": "Cycle Minimum (ms):",
        "mode_selection": "Mode Selection",
        "standard": "Standard",
        "series": "Series",
        "cumulative": "Cumulative",
        "advanced_actions": "Advanced Actions",
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
        "starting_routine": "starting routine"
    },
    "es": {
        "title": "Trainer-app",
        "language": "Idioma:",
        "exercises": "Lista de Ejercicios (separados por comas):",
        "cycle_time": "Ciclo (s):",
        "min_reduction": "Reducción Mínima (ms):",
        "max_reduction": "Reducción Máxima (ms):",
        "min_cycle": "Mínimo de Ciclos (ms):",
        "mode_selection": "Selección de Modo",
        "standard": "Estándar",
        "series": "Series",
        "cumulative": "Acumulativo",
        "advanced_actions": "Acciones Avanzadas",
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
        "starting_routine": "iniciando rutina"
    }
}

current_language = "en"

def set_language(lang):
    global current_language
    current_language = lang

def get_text(key):
    return TEXTS.get(current_language, TEXTS["en"]).get(key, key)