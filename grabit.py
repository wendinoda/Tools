import os
import urllib
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
import requests
import argparse

def openURL(file_name, url):
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    #meta = u.info()
    file_size = int(u.getheader("Content-Length")[0])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status)
    f.close()

def processURL(url, file_type):
    if file_type == 'base':
        file_name = url.split('/')[-1]
        openURL(file_name, url)
    else:
        dirCrawler(url, file_type)

def dirCrawler(url, file_type):
    #path = url.split('/')[-2]
    path = urlparse(url)
    for root, dirs, files in os.walk(path):
        for _file in files:
            _file_name, file_ext = os.path.splitext(_file)
            for file_ext in file_type:
                openURL(_file_name +"."+ file_ext, url)

def getHyperlinks(url, file_type):
    page = urllib.request.urlopen(url)
    soup = bs(page)
    links = []

    for link in soup.find_all('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="download files")
    parser.add_argument('url', metavar='url', type=str, help = 'enter the url of the download path')
    parser.add_argument('file_type', metavar ='file type', type=str ,
            help = 'enter file type. vd for videos ,ad for audio, doc for doc, pdf, xls, ppt ')
    args = parser.parse_args()
    url = args.url
    if args.file_type == 'vd':
        file_type = ["mp4", "webm", "flv", "avi"]
    elif args.file_type == 'ad':
        file_type = ["mp3", "wav"]
    elif args.file_type == 'doc':
        file_type =["pdf", "doc", "xls", "ppt"]
    elif args.file_type == 'img':
        file_type = ["jpg", "jpeg", "png", "gif"]
    else:
        file_type = "base"
    processURL(url, file_type)
