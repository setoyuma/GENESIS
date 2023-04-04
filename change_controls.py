import json

def load():
    with open('settings.json', 'w') as f:
        f.write(json.dumps())

def save():
    pass