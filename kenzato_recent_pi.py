#!/usr/bin/python3

import urllib3, bs4, requests
import urllib.request
import time

###   Define GLOBALS   ###

url = 'https://www.kenzato.uk/booru/explore/recent/'
html = '/home/trestles/resilio/scripts/kenzato/kenzato_recent.html'
downloaded = '/home/trestles/resilio/scripts/kenzato/downloaded.txt'
downloaded_new = '/home/trestles/resilio/scripts/kenzato/downloaded_new.txt'
dest_dir = '/home/trestles/resilio/temp/'

#  Timestamp for cron logs  #
ts = time.localtime()
readable = (time.strftime("%Y-%m-%d %H:%M:%S", ts))

###   Pull the full HTML of the "Recents" page and store in HTML   ###


print ("----- Kenzato Pi Download " + readable + " -----")
#print ("Building 'RECENTS' html file...")
print ("Fetching Kenzato Recents...")

http = urllib3.PoolManager()
r = http.request('GET', url)

web_data = str(r.data)

with open(html, 'w') as f:
    f.write(web_data)
    
###   Parse recently created HTML file for the 24 links to fetch images from and save to array  ###

kenzato = open(html)
html_soup = bs4.BeautifulSoup(kenzato.read(), "html.parser")

link = html_soup.select('.image-container')

#print ("Generating LINKS arrays...")

#  Parse out ALL "recent" links and save to array  #
n = 0
links = []
while n <= 23:
    links.append(link[n].get('href'))
    n = n + 1

#  Write parsed out links to file to prepare comparison  #
open(downloaded_new, 'w').close()
with open(downloaded_new, 'a') as f:
    for i in links:
        f.write(str(i + '\n'))  
    
###   Prepare to explore links   ###

print ("Searching for new links...")

#  While loop to check for duplicate links that have already been explored and save new links to array  #
to_dl = []
loop = 0
attempt = 0
new_files = 0
while attempt<=23 and True:
    for s in links:
        if s in open(downloaded).read():
            loop = loop + 1
            attempt = attempt + 1
        else:
            to_dl.append(s)
            loop = loop - 1
            attempt = attempt + 1
            new_files = new_files + 1
            

###   Continue script based on outcome of above WHILE group   ###

#  If no new files were find, declare it and terminate script  #
if loop == 24:
    print ("There are no new files to download." )
    
#  If new links were find, continue script to search and download card files  #
else:
    print ("Found " + str(new_files) + " files to download!")
    print ("--- Downloading new images ---")
    for s in to_dl: 

        #  Parse new link HTML #
        r2 = requests.get(s)
        r2_soup = bs4.BeautifulSoup(r2.text, "html.parser")

        #  Search for original image link  #
        image = r2_soup.find('meta', attrs={"property": "og:image"})
        chara_link = (image.get('content'))

        #  Search for group tag (hs2, kk, etc)  #
        tag = r2_soup.select('.description-meta')
        tag2 = r2_soup.find('a', attrs={"rel":"tag"})
        group = tag2.text

        #  Get chara card file name  #
        chara_card = chara_link.split('/')[-1]

        #  Define grabber as browser  #
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        
        #  Download and sort file based on group tag  #
        if group == "5 Koikatsu":
            print ("Downloading CharaCard" + chara_card + " for Koikatsu.")
            urllib.request.urlretrieve(chara_link, (dest_dir + "kk/" + chara_card))
            
        elif group == "A AI Syoujyo Cards" or group == "C HS2 Cards":
            print ("Downloading CharaCard" + chara_card + " for HoneySelect2.")
            urllib.request.urlretrieve(chara_link, (dest_dir + "hs2/" + chara_card))
            
        elif group == "6 KK Scenes":
            print ("Downloading Scene" + chara_card + " for Koikatsu.")
            urllib.request.urlretrieve(chara_link, (dest_dir + "kksc/" + chara_card))
            
        elif group == "D HS2 Scenes" or group == "B AI Syoujyo Scenes":
            print ("Downloading Scene" + chara_card + " for Honey Select 2.")
            urllib.request.urlretrieve(chara_link, (dest_dir + "hs2sc/" + chara_card))
        
        elif group == "7 HSU (1.0 cards)" or group == "8 HSU Scenes(1.0 scenes)":
            print ("Downloading CharaCard" + chara_card + " for HSU 1.")
            urllib.request.urlretrieve(chara_link, (dest_dir + "questionable/HSU1/" + chara_card))
            
        else:
            print ("Downloading CharaCard" + chara_card + " with unknown group.")
            urllib.request.urlretrieve(chara_link, (dest_dir + "questionable/" + chara_card))
                
        #  If successful, append link to downloaded.txt to avoid redundancy  #
        with open(downloaded, 'a') as f:
            f.write(s + '\n')

# Print new line for cron log  #
print ("\n")
