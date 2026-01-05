import random
import time
import threading

routine_state = {
    "running": False,
    "current_exercise": None,
    "current_series": [],
    "thread": None,
    "status_callback": None,
    "config": {}
}

def configure_routine(exercises, cycle_time, min_reduction, max_reduction, min_cycle, 
                     mode, serre, serin, serde, cumre):
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
        "cumre": cumre
    }

def set_status_callback(callback):
    routine_state["status_callback"] = callback

def prepare_routine(audio_module):
    if routine_state["status_callback"]:
        routine_state["status_callback"]("preparing", None, 0, 0)
    
    exercises = routine_state["config"]["exercises"]
    for exercise in exercises:
        audio_module.generate(exercise.strip())
    
    audio_module.clean(exercises)

def start_routine(audio_module):
    if routine_state["running"]:
        return
    
    routine_state["running"] = True
    routine_state["current_series"] = []
    routine_state["thread"] = threading.Thread(target=lambda: run_routine(audio_module), daemon=True)
    routine_state["thread"].start()

def stop_routine():
    routine_state["running"] = False
    if routine_state["thread"]:
        routine_state["thread"].join(timeout=1)

def is_running():
    return routine_state["running"]

def run_routine(audio_module):
    prepare_routine(audio_module)
    config = routine_state["config"]
    current_cycle_time = config["cycle_time"]
    
    while routine_state["running"]:
        if config["mode"] == 0:
            execute_standard(audio_module, current_cycle_time)
        elif config["mode"] == 1:
            execute_series(audio_module, current_cycle_time)
        elif config["mode"] == 2:
            execute_cumulative(audio_module, current_cycle_time)
        
        reduction = random.randint(config["min_reduction"], config["max_reduction"]) / 1000
        current_cycle_time = max(config["min_cycle"], current_cycle_time - reduction)

def execute_standard(audio_module, cycle_time):
    config = routine_state["config"]
    exercise = random.choice(config["exercises"])
    routine_state["current_exercise"] = exercise
    
    if routine_state["status_callback"]:
        routine_state["status_callback"]("running", exercise, 0, cycle_time)
    
    audio_module.play(exercise)
    wait_cycle(cycle_time)

def execute_series(audio_module, cycle_time):
    config = routine_state["config"]
    
    if not routine_state["current_series"]:
        routine_state["current_series"] = [random.choice(config["exercises"])]
    else:
        rand_val = random.randint(0, 100)
        
        if rand_val < config["serin"]:
            max_size = len(config["exercises"]) if config["serre"] else len(set(routine_state["current_series"])) + 1
            if len(routine_state["current_series"]) < max_size:
                available = config["exercises"] if config["serre"] else [e for e in config["exercises"] if e not in routine_state["current_series"]]
                if available:
                    routine_state["current_series"].append(random.choice(available))
        elif rand_val < config["serin"] + config["serde"] and len(routine_state["current_series"]) > 1:
            routine_state["current_series"].pop()
    
    
    if routine_state["status_callback"]:
        routine_state["status_callback"]("running", routine_state["current_series"].copy(), 0, cycle_time)
    
    for i, exercise in enumerate(routine_state["current_series"]):
        if not routine_state["running"]:
            return
        
        routine_state["current_exercise"] = exercise
        audio_module.play(exercise)
        time.sleep(0.5)
    
    remaining_time = cycle_time - (len(routine_state["current_series"]) * 0.5)
    if remaining_time > 0:
        wait_cycle(remaining_time, routine_state["current_series"].copy())

def execute_cumulative(audio_module, cycle_time):
    config = routine_state["config"]
    
    if not routine_state["current_series"]:
        routine_state["current_series"] = [random.choice(config["exercises"])]
    else:
        available = config["exercises"] if config["cumre"] else [e for e in config["exercises"] if e not in routine_state["current_series"]]
        if available:
            routine_state["current_series"].append(random.choice(available))
    
    
    if routine_state["status_callback"]:
        routine_state["status_callback"]("running", routine_state["current_series"].copy(), 0, cycle_time)
    
    for i, exercise in enumerate(routine_state["current_series"]):
        if not routine_state["running"]:
            return
        
        routine_state["current_exercise"] = exercise
        audio_module.play(exercise)
        time.sleep(0.5)
    
    remaining_time = cycle_time - (len(routine_state["current_series"]) * 0.5)
    if remaining_time > 0:
        wait_cycle(remaining_time, routine_state["current_series"].copy())

def wait_cycle(duration, series=None):
    start_time = time.time()
    while routine_state["running"] and (time.time() - start_time) < duration:
        elapsed = time.time() - start_time
        remaining = duration - elapsed
        if routine_state["status_callback"]:
            display_exercise = series if series else routine_state["current_exercise"]
            routine_state["status_callback"]("running", display_exercise, elapsed, remaining)
        time.sleep(0.1)