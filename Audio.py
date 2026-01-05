import io
import wave
import pyttsx3
import pyaudio
from pydub import AudioSegment


_cache = {}
_language = 'es'


def set_language(language):
    global _language
    _language = language


def generate(word):
    if word in _cache:
        return
    
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    for voice in voices:
        if _language in voice.languages or _language in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    
    audio_buffer = io.BytesIO()
    engine.save_to_file(word, 'temp_audio.wav')
    engine.runAndWait()
    
    audio_segment = AudioSegment.from_wav('temp_audio.wav')
    _cache[word] = audio_segment
    
    import os
    os.remove('temp_audio.wav')


def play(*words):
    if not words:
        return
    
    segments = []
    pause = AudioSegment.silent(duration=5)
    
    for i, word in enumerate(words):
        if word not in _cache:
            generate(word)
        
        segments.append(_cache[word])
        
        if i < len(words) - 1:
            segments.append(pause)
    
    combined = sum(segments)
    
    audio_data = io.BytesIO()
    combined.export(audio_data, format='wav')
    audio_data.seek(0)
    
    with wave.open(audio_data, 'rb') as wf:
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                       channels=wf.getnchannels(),
                       rate=wf.getframerate(),
                       output=True)
        
        chunk_size = 1024
        data = wf.readframes(chunk_size)
        
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)
        
        stream.stop_stream()
        stream.close()
        p.terminate()


def ready(word):
    return word in _cache


def clean(words=None):
    global _cache
    
    if words is None:
        _cache.clear()
    else:
        words_to_keep = set(words) if not isinstance(words, set) else words
        _cache = {word: audio for word, audio in _cache.items() 
                 if word in words_to_keep}