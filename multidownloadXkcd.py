#! python3
# multidownloadXkcd.py - Downloads XKCD comics using multiple threads.

import requests, os, bs4, threading
os.makedirs('xkcd', exist_ok=True) # store comics in ./xkcd

def processSharepoint(): 
    print('Trying to open the sharepoint root file')
    #res = requests.get('C:\Design\PROJECTS\MOLER\Multithread download\sharepoint root.html')
    #res.raise_for_status()

    rootfile = open('C:\Design\PROJECTS\MOLER\Multithread download\sharepoint root.txt')
    soup = bs4.BeautifulSoup(rootfile.read())
    rootfile.close()

    folderElements = soup.select('script')
    
    if folderElements == []:
        print('Did not find anything')
    else:
        for folderElement in folderElements:
            if folderElement.extract():
                print('Found ListData')
            else:
                print('Did not find anything')

def downloadXkcd(startComic, endComic):
    for urlNumber in range(startComic, endComic):
        try:
            # Download the page.
            print('Downloading page http://xkcd.com/%s...' % (urlNumber))
            res = requests.get('http://xkcd.com/%s' % (urlNumber))
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text)

            # Find the URL of the comic image.
            comicElem = soup.select('#comic img')
            if comicElem == []:
                print('Could not find comic image.')
            else:
                comicUrl = comicElem[0].get('src')
                # Download the image.
                print('Downloading image %s...' % (comicUrl))
                res = requests.get('https:' + comicUrl)
                res.raise_for_status()

                # Save the image to ./xkcd
                urlString = str(urlNumber)
                prefix = ''
                for i in range(5,len(urlString),-1):
                    prefix = '0' + prefix
                urlString = prefix + urlString + '_'

                imageFile = open( os.path.join('xkcd', urlString + os.path.basename(comicUrl)), 'wb')
                for chunk in res.iter_content(100000):
                    imageFile.write(chunk)
                imageFile.close()
        except Exception as exc:
            print('There was a problem %s' %(exc))

# Create and start the Thread objects.
downloadThreads = [] # a list of all the Thread objects
downloadThread = threading.Thread(target=processSharepoint)
downloadThreads.append(downloadThread)
downloadThread.start()
"""
for i in range(1200, 1401, 10): # loops, creates threads
    downloadThread = threading.Thread(target=downloadXkcd, args=(i, i + 99))
    downloadThreads.append(downloadThread)
    downloadThread.start()

# Wait for all threads to end.
for downloadThread in downloadThreads:
    downloadThread.join()"""
print('Done.')
