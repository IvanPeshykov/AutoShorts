import srt, random, os

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

def format_song(song_path : str):
    if os.path.isdir(song_path):
        files = os.listdir(song_path)
        if not files:
            raise ValueError("Songs folder that you provided is empty!")
        return os.path.join(song_path, random.choice(files))
    
    return song_path

def get_random_item(items):
    return items[random.randint(0, len(items) - 1)]