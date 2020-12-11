import os
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

"""
@author: Ping
"""

def getURLFromWebsite(url_, inputfiles_):
    page_count, url_count = 0, 0
    while True:
        URL = url_ + str(page_count + 1)
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", itemprop="url")
        urls = []
        for result in results:
            urls.append(result.get("href"))
        urls.pop(0)
        if len(urls) == 0:
            break
        page_count += 1
        for url in urls:
            if url not in inputfiles_:
                url_count += 1
                outfile.write(url + "\n")
                inputfiles_.append(url)
            print("\rpage " + str("%03d" % page_count) + " url " +
                  str("%04d" % url_count),
                  end='')
    print()
    return


def getPictureURLFromPageURL(urls_, inputfile_pics_):
    url_count, pic_count = 0, 0
    for url in urls_:
        url_count += 1
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("img", itemprop="image")
        pics = []
        for result in results:
            pics.append(result.get("src"))
        for pic in pics:
            if pic not in inputfile_pics_:
                pic_count += 1
                outfile.write(pic + "\n")
                inputfile_pics_.append(pic)
            print("\rurl " + str("%04d" % url_count) + " pic " +
                  str("%06d" % pic_count),
                  end='')
    print()
    return


def savePictureFromPictureURL(pics_):
    pic_count = 0
    for pic in pics_:
        pic_count += 1
        localpath = os.path.join("D:/Programming/picture/" +
                                 str("%06d" % pic_count) + ".png")
        print("\rpic " + str("%06d" % pic_count), end='')
        urlretrieve(pic, localpath)
    print()
    return


# pre stage
URL_FileName = "url.txt"
PIC_FileName = "pic.txt"
URL_ORG = "https://www.niji-wired.info/page/"

# stage 1
outfile = open(URL_FileName, 'a')
infile = open(URL_FileName, 'r')
inputfile = infile.read()
inputfiles = inputfile.split("\n")

getURLFromWebsite(URL_ORG, inputfiles)

infile.close()
outfile.close()

# stage 2
infile_url = open(URL_FileName, 'r')
inputfile_url = infile_url.read()
urls = inputfile_url.split("\n")

outfile = open(PIC_FileName, 'a')
infile_pic = open(PIC_FileName, 'r')
inputfile_pic = infile_pic.read()
inputfile_pics = inputfile_pic.split("\n")

getPictureURLFromPageURL(urls, inputfile_pics)

infile_url.close()
infile_pic.close()
outfile.close()

# stage 3
infile_pic = open(PIC_FileName, 'r')
inputfile_pic = infile_pic.read()
pics = inputfile_pic.split("\n")

savePictureFromPictureURL(pics)

infile_pic.close()
