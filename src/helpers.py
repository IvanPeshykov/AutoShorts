import srt
import random
from constants import fonts

def format_srt(file_path):
    # Read in the file
    with open(file_path, 'r') as file:
        filedata = file.read()

    subs = list(srt.parse(filedata))
    
    for sub in subs:
        sub.content = sub.content.upper()

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(srt.compose(subs))
    
    file.close()

def get_random_font():
    return fonts[random.randint(0, len(fonts) - 1)]
