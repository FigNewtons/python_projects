import os, re
from mutagen.easyid3 import EasyID3


def read_tags(path, folder=False, encoding='mp3'):
    """Print out existing tags. """
    if folder:
        songs = [f for f in os.listdir(path) if encoding in f]
        for song in songs:
            audio = EasyID3(path + '/' + song)
            print(audio.pprint())
    else:
        audio = EasyID3(path)
        print(audio.pprint() + '\n')


# TODO: Fix argument list so that *keys works
def read_fields(path, *keys, folder=False, encoding='mp3'):
    """Print out specific fields from existing tags. """
    valid_keys = EasyID3.valid_keys.keys()
    keys = [k for k in keys if k in valid_keys]
    
    if folder:
        songs = [f for f in os.listdir(path) if encoding in f]
        for song in songs:
            audio = EasyID3(path + '/' + song)
            print('Song: ' + song)
            for k in keys:
                print(k + ": " + audio[k])
    else:
        audio = EasyID3(path)
        print('Song: ' + song)
        for k in keys:
            print(k + ": " + audio[k])


def update_tags(path, folder=False, encoding='mp3', **fields):    
    """Update field value(s) for a tag / set of tags. """
    keys = sorted(fields.keys())
    valid_keys = EasyID3.valid_keys.keys()
    
    keys = [k for k in keys if k in valid_keys]
    
    if folder:
        songs = [f for f in os.listdir(path) if encoding in f]
        for song in songs:
            try:
                audio = EasyID3(path + '/' + song)
                print('Song: ' + song)
                for k in keys:
                    audio[k] = fields[k]
                    print('Updated field: ' + k + ':' + fields[k])
            except:
                print('Failed to update for song: ' + song)
    else:
        try:
            audio = EasyID3(path)
            for k in keys:
                audio[k] = fields[k]
                print('Updated field: ' + k + ':' + fields[k])
            audio.save()
        except:
            print('Failed to update')


def delete_tags(path, folder=False, encoding='mp3'):
    """Delete the entire tag. """
    if folder:
        songs = [f for f in os.listdir(path) if encoding in f]
        for song in songs:
            audio = EasyID3(path + '/' + song)
            try:
                audio.delete()
                print('Deleted tags for: ' + song)
            except:
                print('Failed to delete tags for: ' + song)
    else:
        audio = EasyID3(path)
        try:
            audio.delete()
            print('Deleted tags')
        except:
            print('Failed to delete tags')


# TODO: Include album cover in tag.
def tag_album(path, genre, encoding='mp3', discno='1/1', test=False):
    """Create tag for every song in a given album.
    
    By default, each tag has the following fields:
        -Album
        -Artist
        -Date  (Album release date)
        -Disc Number
        -Genre
        -Title
        -Track Number
    
    Args:
        path: Path to the album directory
        genre: Album genre (e.g. 'Rock, 'Indie', 'Jazz')
        encoding: Song encoding (e.g. 'mp3', 'm4a', 'flac'); only mp3
                is supported at the moment
        discno: Disc Number / Total Number of Discs in Album set
        test: This option allows you to view what information is written
                to the tags before actually doing it

    Note:
        The function makes a few assumptions regarding the path
        and song format (based on a convention I picked). First,
        the path argument takes the form:
        
            "~/music/albums/'Artist'/'Album (Year)'"

        where Year is four digits. Second, each song takes the form:
            
            "xx. Song Title.mp3"

        where xx is a two-digit number (e.g. 05, 12). Last, album covers
        have the relative path "artwork/cover.jpg" from the album
        directory. 
    """
    year_regex = '\((\d{4})\)$'
    song_regex = '^(\d{2})\. (.+).' + encoding

    art, alb = path.split('/')[-2:]

    artist = art
    year = re.search(year_regex, alb).group(0)
    album = alb.split(year)[0].strip()

    # Strip parentheses
    date = year[1:5]

    songs = [f for f in os.listdir(path) if encoding in f]
    total = str(len(songs))

    for song in songs:
        match = re.search(song_regex, song)
        trackno, title = match.groups()
        
        if trackno[0] == '0':
            trackno = trackno[1]
        trackno = trackno + '/' + total
        
        if test:
            print("Album: ", album)
            print("Artist: ", artist)
            print("Date: ", date)
            print("Disc No: ", discno)
            print("Genre: ", genre)
            print("Title: ", title)
            print("Track No: ", trackno)
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
                print(audio.pprint() + '\n')



