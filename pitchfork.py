'''
    pitchfork.py
    Fig Newtons
 
    June 12, 2015

    Fetches album info from 'Best New Albums' section of pitchfork.com

    Currently, this program is very basic, but I may aggregate album info
    from multiple sites to get more complete information 
'''

from lxml import html
import requests
import operator
import time

class AlbumRating:
    # TODO: Find sources that supply genre, release date, number of tracks
    def __init__(self, tag):
        self.artist = tag[0]
        self.album_name = tag[1]
        self.rating = tag[2]

    def __str__(self):
        display = 'Album: {0}\nArtist: {1}\nRating: {2}\n'
        return display.format(self.album_name, self.artist, self.rating)

    def is_self_titled_EP:
        return self.artist == self.album_name



# URL and No. of Albums to Retrieve
url = "http://pitchfork.com/reviews/best/albums/"
ALBUM_LIMIT = 20

# XPath strings to retrieve artist, album, and score
xart = '//div[@class="info"]/a/h1/text()'
xalb = '//div[@class="info"]/a/h2/text()'
xrate = '//div[@class="info"]/span/text()'

# Get Current Time
now = time.strftime("%c")

# List of album data
tag = []
pagecount = 1

while len(tag) < ALBUM_LIMIT: 
    page = requests.get(url + str(pagecount))
    tree = html.fromstring(page.text)

    artists = tree.xpath(xart)
    albums = tree.xpath(xalb)
    ratings = tree.xpath(xrate)

    # I should check that these are same length
    batch = list(zip(artists, albums, ratings))

    tag += batch 
    pagecount += 1


new_albums = [ AlbumRating(data) for data in tag[:ALBUM_LIMIT]]

# Sort list
new_albums.sort(key = operator.attrgetter('rating'), reverse = True)

# Output List
print("20 Best New Albums according to Pitchfork \nRetrieved " + now + "\n\n") 
for album in new_albums:
    print(album)



