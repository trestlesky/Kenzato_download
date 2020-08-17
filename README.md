# Kenzato_download
Python script to automate downloading and sorting Illusion Cards from the "Recent" section on Kenzato Booru. 

DISCLAIMER: I am not a developer, but use Python to automate multiple tasks for my own personal projects. I don't consider myself an epxert at all, but do consider myself to be a strong beginner/weak intermediate user/writer of Python scripts. I know I don't follow best practices, but always welcome feedback. 

With the DISCLAIMER in mind, I know that this script isn't perfect. For me, it was a great self-taught lesson on BeautifulSoup parsing HTML with python, and urllib for downloading files.  Some things I would like to do:

1) Wrap some parts in functions.
2) Clean up/simplify loops.
3) If possible, move away from depending on outside files, such as downloaded.txt, downloaded_new.txt, and html file. 

Description of script code can be found as comments in the script itself. The general idea of the script is to:

1) Fetch HTML from https://www.kenzato.uk/booru/explore/recents
2) From HTML, generate a list of "recent" uploads (by link)
3) Compare list of "recents" to "downloaded" list to find new uploads.
4) Download new uploaded cards/files and sort them based on site tags (Koikatsu, HoneySelect2, scenes, etc). 

If you plan to use this script yourself, make sure you change the globals to match your particular setting (i.e. paths will need to be changed). Remember, this is a template, so use to your best fit. 

I run this from a raspberry pi as a cronjob every half hour. If you decided to schedule it, please be respectful of the web server owner. Don't set it to run every 30 secs or something, 20-30 min is plenty far apart. 

Any questions/feedback can be sent to trestlesky@yahoo.com
