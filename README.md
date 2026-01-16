# ![Logo](Icon.png)Trainer-app

## About App
A Python-based coaching assistant featuring dynamic TTS audio feedback. Generates random, serial, and cumulative workout routines with customizable timing and multilingual support.

## Features
* Exercise Input: Text field for comma-separated exercises.
* Time Configuration: Fields for cycle time and random time reduction.
* Multiple Modes: Standard (single), Series, or Cumulative.

## How to use
1. Write your exercise plan in the "Exercise List" field.
2. Set your time settings for the session:
    * Cycle Time: Time in seconds between exercises.
    * Reduction Maximum and Minimum: Randomized reduction value in milliseconds for the Cycle Time.
    * Cycle Min: Minimum time the Cycle Time can reach after reductions.

3. Set your preferred mode:
    * Standard Mode: Randomly selects and announces exercises with variable wait times.
    * Series Mode: Randomly selects multiple exercises with adjustable probabilities for increasing or decreasing the quantity.
    * Cumulative Mode: Randomly selects accumulating sequences; optional repeats, stops if no more unique exercises remain.
4. Start training.

## Important Note on Antivirus Detection
Some antivirus programs may flag this executable as a potential threat or "unrecognized software". Please be assured that this is a false positive. 

## Creator support
If this tool helped you track your progress or if you find the project useful, consider supporting my work! Every donatios helps me:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/H2H11RMG69) [![Invitame un café en cafecito.app](https://cdn.cafecito.app/imgs/buttons/button_3.svg)](https://cafecito.app/ijcs)

## Libraries Used
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- [PyAudio](https://github.com/jleb/pyaudio)
- [pydub](https://github.com/jiaaro/pydub)

## Known Issues
* **Static Help Text:** The help text does not currently update when the application language is changed.
* **Series Mode Malfunction:** The "Series Mode" is not operating as intended. It currently functions as a cumulative mode rather than its designated behavior.
