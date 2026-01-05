import configparser
import os

CONFIG_FILE = "Trainer-config.ini"

def _get_config():
    config = configparser.ConfigParser()
    
    if not os.path.exists(CONFIG_FILE):
        _create_default_config()
    
    config.read(CONFIG_FILE)
    return config

def _create_default_config():
    config = configparser.ConfigParser()
    
    config['General'] = {
        'Lang': 'en'
    }
    
    config['Profile'] = {
        'ExeLis': '1, 2, 3, 4, 5',
        'CycleT': '1',
        'MaxRT': '50',
        'MinRT': '0',
        'CyMin': '5',
        'Mode': '0'
    }
    
    config['Advanced'] ={
        'SerRe': 'False',
        'SerIn': '100',
        'SerDe': '0',
        'CumRe': 'True'
    }
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def General(option):
    config = _get_config()
    return config.get('General', option)

def Profile(option):
    config = _get_config()
    return config.get('Profile', option)

def Advanced(option):
    config = _get_config()
    return config.get('Advanced', option)

def Set(section, option, value):
    config = _get_config()
    
    if not config.has_section(section):
        config.add_section(section)
    
    config.set(section, option, str(value))
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
        
_get_config()