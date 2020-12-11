import os
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options

from PIL import Image
from PIL import ImageFile
"""
@author: Ping
"""


def getBookURLFromWebsite(FilePath_, urlOriginal_):
    options = Options()
    options.add_argument("--disable-notifications")
    newChromeWindow = webdriver.Chrome(FilePath_, options=options)
    newChromeWindow.minimize_window()
    newChromeWindow.get(urlOriginal_)

    soup = BeautifulSoup(newChromeWindow.page_source, "html.parser")
    newChromeWindow.close()

    urlResults = []
    # 1 for 話 2 for 卷
    result = str(soup.find(id="detail-list-select-2"))
    while result.find(" href") != -1:
        result = result[result.find(" href") + 5:]
        urlResults.append(result[result.find("=\"/") + 3:result.find("/\" ")])
    urlResults.pop(0)
    urlResults.reverse()
    # urlResults.pop(0)
    return urlResults


def getBookPageURLFromWebsite(FilePath_, urlResults_, inputFiles_, urlBase_):
    articleCounter = 0
    for urlResult in urlResults_:
        articleCounter += 1
        if str(articleCounter) in inputFiles_:
            continue

        options = Options()
        options.add_argument("--disable-notifications")
        urlAppend = urlBase_ + urlResult
        newChromeWindow_tmp = webdriver.Chrome(FilePath_, options=options)
        newChromeWindow_tmp.minimize_window()
        newChromeWindow_tmp.get(urlAppend)

        pageCounter = 0
        pageResults = []

        while True:
            soup = BeautifulSoup(newChromeWindow_tmp.page_source,
                                 "html.parser")
            result = str(soup.find(id="cp_img"))
            result = result[result.find(" src"):]
            result = result[result.find("https"):result.find("?")]
            if result.find("mshowmanga") == -1:
                pageResults.append(result)
                element = newChromeWindow_tmp.find_element_by_class_name(
                    "win-pay-title2")
                newChromeWindow_tmp.execute_script("nextPage();")
                pageCounter += 1
                if element.location != {'x': 0, 'y': 0}:
                    break
        newChromeWindow_tmp.close()
        print(str("%03d" % articleCounter), str("%03d" % pageCounter), '\n')
        outFile.write(str(articleCounter) + "\n")
        for pageResult in pageResults:
            outFile.write(pageResult + "\n")
        outFile.write("\n")
    return


def savePictureFromURL(pics_, inputPicFiles_, PicPathBase_):
    articleCounter, pageCounter = 0, 0
    for pic in pics_:
        if pic.find("http") == -1:
            if pic != "":
                tmp = str("%03d" % articleCounter) + str("%03d" % pageCounter)
                if tmp not in inputPicFiles_ and articleCounter * pageCounter != 0:
                    outPicFile.write(tmp + "\n")
                articleCounter += 1
                pageCounter = 0
        else:
            pageCounter += 1
            localpath = os.path.join(PicPathBase_ +
                                     str("%03d" % articleCounter) + "_" +
                                     str("%03d" % pageCounter) + ".png")
            print("\r" + str("%03d" % articleCounter) + " " +
                  str("%03d" % pageCounter),
                  end='')
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(pic, localpath)
    print()
    return


def savePictureToPDF(inputPicFiles_, PicPathBase_):
    imageCounter = 0
    for picNumber in inputPicFiles_:
        articleNumber = picNumber[:3]
        pageTotal = picNumber[3:]
        if pageTotal[0] == '0':
            pageTotal = pageTotal[1:]
        pageTotal = int(pageTotal)

        imageList = []
        for pageCounter in range(pageTotal):
            tmp = pageCounter + 1
            inputImage = Image.open(PicPathBase_ + articleNumber + "_" +
                                    str("%03d" % tmp) + ".png")
            inputImage = inputImage.convert('RGB')
            imageList.append(inputImage)

            imageCounter += 1
            print("\r" + str("%04d" % imageCounter), end="")

        imageList.pop(0)
        inputImageNew = Image.open(PicPathBase_ + articleNumber + "_001.png")
        inputImageNew.save(PicPathBase_ + articleNumber + ".pdf",
                           save_all=True,
                           append_images=imageList)
    return


# pre stage
url_FileName = "url.txt"
pic_FileName = "pic.txt"
FilePath = "D:/Programming/Python/WebCrawler/chromedriver.exe"
urlBase = "https://www.manhuaren.com/"
urlOriginal = "https://www.manhuaren.com/manhua-jinjidejuren/"
PicPathBase = "D:/Programming/picture/"

# stage 1
outFile = open(url_FileName, 'a')
inFile = open(url_FileName, 'r')
inputFile = inFile.read()
inputFiles = inputFile.split("\n")

URL_Results = getBookURLFromWebsite(FilePath, urlOriginal)
getBookPageURLFromWebsite(FilePath, URL_Results, inputFiles, urlBase)

inFile.close()
outFile.close()

# stage 2
inFile_pic = open(url_FileName, 'r')
inputFile_pic = inFile_pic.read()
pics = inputFile_pic.split("\n")

outPicFile = open(pic_FileName, 'a')
inPicFile = open(pic_FileName, 'r')
inputPicFile = inPicFile.read()
inputPicFiles = inputPicFile.split("\n")

savePictureFromURL(pics, inputPicFiles, PicPathBase)

inFile_pic.close()
inPicFile.close()
outPicFile.close()

# stage 3
ImageFile.LOAD_TRUNCATED_IMAGES = True

inPicFile = open(pic_FileName, 'r')
inputPicFile = inPicFile.read()
inputPicFiles = inputPicFile.split("\n")

savePictureToPDF(inputPicFiles, PicPathBase)

inPicFile.close()
