#!/usr/bin/python3

import urllib3, bs4, requests
import urllib.request
import time

###   Define GLOBALS   ###
url = 'https://www.kenzato.uk/booru/explore/recent/'
html = '/path/to/htmlfile.html'
downloaded = '/path/to/downloaded.txt'
downloaded_new = '/path/to/downloaded_new.txt'
failed = '/path/to/failed.txt
dest_dir = '/path/to/download/destination/'

#  Timestamp for cron logs  #
ts = time.localtime()
readable = (time.strftime("%Y-%m-%d %H:%M:%S", ts))

###   Pull the full HTML of the "Recents" page and store in HTML file   ###

print ("----- Kenzato Pi Download " + readable + " -----")
print ("Fetching Kenzato Recents...")

#  Send GET request to webpage  #
http = urllib3.PoolManager()
r = http.request('GET', url)

#  String out info to write to prepare to write to html file  #
web_data = str(r.data)

#  Write html string to file  #
with open(html, 'w') as f:
    f.write(web_data)
    
###   Parse recently created HTML file for the 24 links to fetch images from and save to array  ###

#  Feed html to BeautifulSoup html parser  #
kenzato = open(html)
html_soup = bs4.BeautifulSoup(kenzato.read(), "html.parser")

#  Links have the ".image-container" html class, so this searches for links in that class  #
link = html_soup.select('.image-container')

#  Parse out ALL "recent" links and save to array  #
#  i.e. ALL 24 links on the recent page or pulled into the "links" array  #
n = 0
links = []
while n <= 23:
    links.append(link[n].get('href'))
    n = n + 1

#  Write parsed out links to downloaded_new.txt file to prepare comparison  #
open(downloaded_new, 'w').close()
with open(downloaded_new, 'a') as f:
    for i in links:
        f.write(str(i + '\n'))  
    
###   Prepare to explore links   ###

print ("Searching for new links...")

#  While loop to check for duplicate links that have already been explored and save new links to array.  #
#  If this is the first time the script runs, "downloaded.txt" will be created and all 24 links added.  #
#  Ultimately, links in downloaded_new.txt are compared to links found in downloaded.txt. 
#  We know there are 24 links, so the while statement runs for 24 times and exits after.  Duplicate  #
#  links are ignored, new links are added to "to_dl" array to be used later.  "attempts" tracks how  #
#  many times the loop runs, "loop" actually tracks total number of duplicate links, and "new_files"  #
#  tracks new links. As you'll see later, if "loop" = 24, then there are no new links to download.  #
#  However, is "loop" is anything besides 24, we know there were new links found, and we can use the  #
#  "to_dl" array to download. 

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

#  As mentioned above, if loop == 24, we know there are no new links. Script terminates. #
if loop == 24:
    print ("There are no new files to download." )
    
#  Otherwise, we print how many files we found and use the links in "to_dl" to download  #
else:
    print ("Found " + str(new_files) + " files to download!")
    print ("--- Downloading new images ---")
    for s in to_dl: 
        
        try:
            #  Parse new link HTML #
            r2 = requests.get(s)
            r2_soup = bs4.BeautifulSoup(r2.text, "html.parser")

            #  Search for original image link  #
            image = r2_soup.find('meta', attrs={"property": "og:image"})
            chara_link = (image.get('content'))

            #  Get chara card file name  #
            chara_card = chara_link.split('/')[-1]

            #  Search for group tag (hs2, kk, etc)  #
            tag = r2_soup.select('.description-meta')
            tag2 = r2_soup.find('a', attrs={"rel":"tag"})
            group = tag2.text

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
                
        except AttributeError:
                #k  Add card link to "failed.txt" and "downloaded.txt" so it doesn't get parsed again.  #
                print (chara_card + " failed somehow, added to failed list.")
                with open(failed, 'a') as f:
                    f.write(s + "\n")
                with open(downloaded, 'a') as f:
                    f.write(s + '\n')


# Print new line for cron log  #
print ("\n")
