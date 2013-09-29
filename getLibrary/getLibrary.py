''' 
------------------- last.fm Library Parser -------------------
Written by: FigNewtons
Date: September 29, 2013

This program stores a list of all of the artists in your 
last.fm library into a plain text file. However, this code
can be modified for more general parsing uses if necessary.

'''
import urllib.request as req

# Replace <username> with your last.fm Username. 
source = 'http://www.last.fm/user/<username>/library?page='
get = '&sortOrder=asc&sortBy=name'
start_tag = '<strong class="name">'
end_tag = '</strong>'

# Change to the number of pages in your library
pages = 50

# Path to blank text file where you want to store the list.
# Make sure the file exists before running this program!
artist_list = '/path/to/file.txt'

# Enumerates the url for each page 
def createURL(source, get):
    for n in range(1, pages + 1):
        url = source + str(n) + get
        getHTML(url)
        print('Page ' + str(n) + ' parsed.')
    return 0

# Makes url request and passes a character stream of the html
def getHTML(url):
    html = req.urlopen(url)
    mybytes = html.read()
    mystr = mybytes.decode("utf8")
    html.close()

    parseHTML(mystr)
    return 0

# Takes character stream and joins into a string. Then outputs 
# an array of the string split by each new line found in the html.
def parseHTML(mystr):
    mystr = ''.join(mystr)
    mystr = mystr.split('\n')

    getList(mystr)
    return 0

# Goes through each line of HTML and if it finds the given start tag, 
# it will extract the value between the start and end tags.
def getList(mystr):
    for line in mystr:
        if start_tag in line:
            artist = line.split(start_tag)[-1]
            artist = artist.split(end_tag)[0]
            writeFile(artist)
    return 0

# Writes artist's name to a text file    
def writeFile(artist):
    f = open(artist_list, 'a+')
    f.write(artist + '\n')
    f.close()

    return 0

# ------------STARTS PROGRAM--------------
createURL(source, get)
