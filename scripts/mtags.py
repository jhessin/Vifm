#!/usr/bin/env python3

import sys
import os
import tempfile
import csv
import mutagen

# Options
editor = os.environ['EDITOR']
attrs = ['artist', 'album', 'title']
escape = '*'

songs = [] # List of mutagen objects
song_attrs = [] # Dictionaries containing attributes to be inspected

ff = sys.argv[1]
default_album_name = os.path.basename(os.path.dirname(os.path.abspath(ff)))
# Make sure mutagen uses the easy version, as
# it uses the normal one by default
extension = os.path.splitext(ff)[1] 
if extension == ".mp3":
    import mutagen.easyid3
    mut_init = mutagen.easyid3.EasyID3
elif extension == ".m4a":
    import mutagen.easymp4
    mut_init = mutagen.easymp4.EasyMP4
else:
    mut_init = mutagen.File

for f in sys.argv[1:]:
    songs.append(mut_init(f))
    song_attrs.append({})
    for attr in attrs:
        song_attrs[-1][attr] = songs[-1].get(attr, [''])[0]
        if not song_attrs[-1][attr]:
            if attr == 'artist':
                _attr = 'albumartist'
                song_attrs[-1][attr] = songs[-1].get(_attr, [''])[0]
            if attr == 'title':
                song_attrs[-1][attr] = os.path.splitext(f)[0]
            if attr == 'album':
                song_attrs[-1][attr] = default_album_name

with tempfile.NamedTemporaryFile('w+', suffix='.csv') as tmpf:
    csvwriter = csv.writer(tmpf, quoting=csv.QUOTE_NONE, escapechar=escape,
            skipinitialspace=True)
    csvwriter.writerows([row.values() for row in song_attrs])
    # Ensure that the file has been written to disk
    tmpf.flush()
    os.system("{} {}".format(editor, tmpf.name))
    tmpf.seek(0)
    csvreader = csv.reader(tmpf, quoting=csv.QUOTE_NONE,
            escapechar=escape, skipinitialspace=True)
    for song,row in zip(songs, csvreader):
        new_song_metadata = dict(zip(attrs, row))
        song.update(new_song_metadata)
        song.save()
