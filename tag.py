import os, re
from mutagen.easyid3 import EasyID3

# Path takes form '~/music/albums/'Artist'/'Album (Year)'

def tag_album(path, genre, encoding = 'mp3', discno = '1/1', test = True):
  
    # Gets 4-digit year in parenthesis at end of string
    year_regex = '\((\d{4})\)$'
    
    # Split song title:  '##. Song Title.mp3'
    song_regex = '^(\d{2})\. (.+).' + encoding


    art, alb = path.split('/')[-2:]

    artist = art
    year = re.search(year_regex, alb).group(0)
    album = alb.split(year)[0].strip()

    # Strip parentheses
    date = year[1:5]

    files = [f for f in os.listdir(path) if encoding in f]
    total = str(len(files))

    for song in files:
        
        m = re.search(song_regex, song)
        trackno, title = m.groups()

        
        if trackno[0] == '0':
            trackno = trackno[1]

        trackno = trackno + '/' + total


        if test:
            tag = "Album: {0}\nArtist: {1}\nDate: {2}\nDiscNo: {3}\nGenre: {4}\nTitle: {5}\nTrackNo: {6}".format(album, artist, date, discno, genre, title, trackno)
            print(tag)
        else:
            try:
                audio = EasyID3(path + "/" + song)
                audio['album'] = album
                audio['artist'] = artist
                audio['date'] = date
                audio['discnumber'] = discno
                audio['genre'] = genre
                audio['title'] = title
                audio['tracknumber'] = trackno
                audio.save()
            except IOError:
                print('Cannot open song: ' + song)
            except (AttributeError, KeyError):
                print('Something wrong with writing tag to file')
            else:
                audio.pprint()



