import random
import time
import threading

routine_state = {
    "running": False,
    "current_exercise": None,
    "current_series": [],
    "thread": None,
    "status_callback": None,
    "config": {},
    "cycle_count": 0,
    "total_time": 0
}

def configure_routine(exercises, cycle_time, min_reduction, max_reduction, min_cycle, 
                     mode, serre, serin, serde, cumre, waitnar):
    routine_state["config"] = {
        "exercises": exercises,
        "cycle_time": cycle_time,
        "min_reduction": min_reduction,
        "max_reduction": max_reduction,
        "min_cycle": min_cycle,
        "mode": mode,
        "serre": serre,
        "serin": serin,
        "serde": serde,
        "cumre": cumre,
        "waitnar": waitnar
    }

def set_status_callback(callback):
    routine_state["status_callback"] = callback

def prepare_routine(audio_module):
    if routine_state["status_callback"]:
        routine_state["status_callback"]("preparing", None, 0, 0, 0)
    
    exercises = routine_state["config"]["exercises"]
    for exercise in exercises:
        audio_module.generate(exercise.strip())
    
    audio_module.clean(exercises)

def start_routine(audio_module):
    if routine_state["running"]:
        return
    
    routine_state["running"] = True
    routine_state["current_series"] = []
    routine_state["cycle_count"] = 0
    routine_state["total_time"] = 0
    routine_state["thread"] = threading.Thread(target=lambda: run_routine(audio_module), daemon=True)
    routine_state["thread"].start()

def stop_routine():
    routine_state["running"] = False
    if routine_state["thread"]:
        routine_state["thread"].join(timeout=2)
        routine_state["thread"] = None
        time.sleep(0.1)

def is_running():
    return routine_state["running"]

def run_routine(audio_module):
    import sys
    if sys.platform == 'win32':
        try:
            import comtypes
            comtypes.CoInitialize()
        except:
            pass
    
    try:
        prepare_routine(audio_module)
        config = routine_state["config"]
        current_cycle_time = config["cycle_time"]
        start_time = time.time()
        
        while routine_state["running"]:
            routine_state["cycle_count"] += 1
            
            if config["mode"] == 0:
                execute_standard(audio_module, current_cycle_time, start_time)
            elif config["mode"] == 1:
                execute_series(audio_module, current_cycle_time, start_time)
            elif config["mode"] == 2:
                execute_cumulative(audio_module, current_cycle_time, start_time)
            
            reduction = random.randint(config["min_reduction"], config["max_reduction"]) / 1000
            current_cycle_time = max(config["min_cycle"], current_cycle_time - reduction)
    finally:
        if sys.platform == 'win32':
            try:
                import comtypes
                comtypes.CoUninitialize()
            except:
                pass

def execute_standard(audio_module, cycle_time, start_time):
    config = routine_state["config"]
    exercise = random.choice(config["exercises"])
    routine_state["current_exercise"] = exercise
    
    routine_state["total_time"] = time.time() - start_time
    
    if routine_state["status_callback"]:
        routine_state["status_callback"]("running", exercise, routine_state["cycle_count"], cycle_time, routine_state["total_time"])
    
    if config["waitnar"]:
        audio_module.play(exercise)
        wait_cycle(cycle_time, start_time)
    else:
        import threading
        threading.Thread(target=lambda: audio_module.play(exercise), daemon=True).start()
        wait_cycle(cycle_time, start_time)

def execute_series(audio_module, cycle_time, start_time):
    config = routine_state["config"]
    
    if not routine_state["current_series"]:
        routine_state["current_series"] = [random.choice(config["exercises"])]
    else:
        rand_val = random.randint(0, 100)
        
        
        if config["serre"]:
            max_size = float('inf')
        else:
            max_size = len(config["exercises"])
        
        if rand_val < config["serin"]:
            if len(routine_state["current_series"]) < max_size:
                available = config["exercises"] if config["serre"] else [e for e in config["exercises"] if e not in routine_state["current_series"]]
                if available:
                    routine_state["current_series"].append(random.choice(available))
                    
        elif rand_val < config["serin"] + config["serde"] and len(routine_state["current_series"]) > 1:
            routine_state["current_series"].pop()
    
    routine_state["total_time"] = time.time() - start_time
    
    if routine_state["status_callback"]:
        routine_state["status_callback"]("running", routine_state["current_series"].copy(), routine_state["cycle_count"], cycle_time, routine_state["total_time"])
    
    for i, exercise in enumerate(routine_state["current_series"]):
        if not routine_state["running"]:
            return
        
        routine_state["current_exercise"] = exercise
        audio_module.play(exercise)
        time.sleep(0.5)
    
    remaining_time = cycle_time - (len(routine_state["current_series"]) * 0.5)
    if remaining_time > 0:
        wait_cycle(remaining_time, start_time, routine_state["current_series"].copy())

def execute_cumulative(audio_module, cycle_time, start_time):
    config = routine_state["config"]
    
    if not routine_state["current_series"]:
        routine_state["current_series"] = [random.choice(config["exercises"])]
    else:
        available = config["exercises"] if config["cumre"] else [e for e in config["exercises"] if e not in routine_state["current_series"]]
        if available:
            routine_state["current_series"].append(random.choice(available))
    
    routine_state["total_time"] = time.time() - start_time
    
    if routine_state["status_callback"]:
        routine_state["status_callback"]("running", routine_state["current_series"].copy(), routine_state["cycle_count"], cycle_time, routine_state["total_time"])
    
    for i, exercise in enumerate(routine_state["current_series"]):
        if not routine_state["running"]:
            return
        
        routine_state["current_exercise"] = exercise
        audio_module.play(exercise)
        time.sleep(0.5)
    
    remaining_time = cycle_time - (len(routine_state["current_series"]) * 0.5)
    if remaining_time > 0:
        wait_cycle(remaining_time, start_time, routine_state["current_series"].copy())

def wait_cycle(duration, start_time, series=None):
    cycle_start_time = time.time()
    while routine_state["running"] and (time.time() - cycle_start_time) < duration:
        routine_state["total_time"] = time.time() - start_time
        if routine_state["status_callback"]:
            display_exercise = series if series else routine_state["current_exercise"]
            routine_state["status_callback"]("running", display_exercise, routine_state["cycle_count"], duration, routine_state["total_time"])
        time.sleep(0.1)