import srt
import random
from constants import fonts, colors

def wrap_with_html_tag(string, tag, attributes=None):
    attribute_string = ""
    if attributes:
        attribute_string = " ".join([f'{key}="{value}"' for key, value in attributes.items()])
    return f"<{tag} {attribute_string}>{string}</{tag}>"

def format_srt(file_path):
    # Read in the file
    with open(file_path, 'r') as file:
        filedata = file.read()

    subs = list(srt.parse(filedata))

    for sub in subs:
        sub.content = sub.content.upper()
        sub.content = wrap_with_html_tag(sub.content, 'span', {"color": get_random_color()})


    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(srt.compose(subs))
    
    file.close()

def get_random_font():
    return fonts[random.randint(0, len(fonts) - 1)]

def get_random_color():
    return colors[random.randint(0, len(colors) - 1)]
