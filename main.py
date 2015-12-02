import logging
import urllib2
import os
import md5
import time

def readHistoryFileMD5():
    md5obj = md5.new()
    fileListRaw = os.listdir(os.getcwd())
    fileListNorth = []
    fileListSouth = []
    for fileName in fileListRaw:
        fileNameSplit = fileName.split('.')
        if fileNameSplit[-1].upper() == 'JPG':
            if fileNameSplit[0][0] == 'N':
                fileListNorth.append(fileNameSplit[0])
            elif fileNameSplit[0][0] == 'S':
                fileListSouth.append(fileNameSplit[0])
    md5LastImageNorth = 0
    md5LastImageSouth = 0
    logging.info('Find %d north image in history.' % len(fileListNorth))
    logging.info('Find %d south image in history.' % len(fileListSouth))
    if len(fileListNorth) != 0:
        fileListNorth.sort()
        newestFileName = fileListNorth[-1]+'.jpg'
        logging.info('The newest north image is %s.' % newestFileName)
        with open(newestFileName,'rb') as hLastImage:
            dataLastImage = hLastImage.read()
            md5obj.update(dataLastImage)
            md5LastImageNorth = md5obj.hexdigest()
    if len(fileListSouth) != 0:
        fileListSouth.sort()
        newestFileName = fileListSouth[-1]+'.jpg'
        logging.info('The newest south image is %s.' % newestFileName)
        with open(newestFileName,'rb') as hLastImage:
            dataLastImage = hLastImage.read()
            md5obj.update(dataLastImage)
            md5LastImageSouth = md5obj.hexdigest()
    return (md5LastImageNorth, md5LastImageSouth)


def getWeatherImage(md5LastImageNorth, md5LastImageSouth):
    urlNorth = 'http://159.226.97.116/getImage?t=1'
    urlSouth = 'http://159.226.97.116/getImage'
    md5NewNorth = md5LastImageNorth
    md5NewSouth = md5LastImageSouth
    try:
        dataNorth = urllib2.urlopen(url=urlNorth, timeout=10).read()
        dataSouth = urllib2.urlopen(url=urlSouth, timeout=10).read()
    except Exception as err:
        logging.error('Fail when getting image from url')
        logging.error(err)
        return (md5NewNorth, md5NewSouth)
    md5obj = md5.new()
    md5obj.update(dataNorth)
    md5NewNorth = md5obj.hexdigest()
    if md5NewNorth != md5LastImageNorth:
        newFileName = 'N' + time.strftime("%Y%m%d%H%M%S") + '.jpg'
        with open(newFileName,'wb') as hNewImage:
            hNewImage.write(dataNorth)
            logging.info('Restored new north image %s' % newFileName)
            print 'Restored new north image %s' % newFileName
    md5obj.update(dataSouth)
    md5NewSouth = md5obj.hexdigest()
    if md5NewSouth != md5LastImageSouth:
        newFileName = 'S' + time.strftime("%Y%m%d%H%M%S") + '.jpg'
        with open(newFileName,'wb') as hNewImage:
            hNewImage.write(dataSouth)
            logging.info('Restored new south image %s' %  newFileName)
            print 'Restored new south image %s' % newFileName
    return (md5NewNorth, md5NewSouth)
    
    
        

def main():
    strTime = time.strftime("%Y%m%d%H%M%S")
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='weatherImage' + strTime + '.log',
                    filemode='w')
    (md5LastImageNorth, md5LastImageSouth) = readHistoryFileMD5()
    lastTime = time.time()
    timeStepSec = 120
    while True:
        time.sleep(20)
        curTime = time.time()
        if curTime - lastTime > timeStepSec:
            (md5LastImageNorth, md5LastImageSouth) = getWeatherImage(md5LastImageNorth, md5LastImageSouth)
            lastTime = curTime
            logging.info('Perform url checking.')
            print 'Perform url checking at %s' % time.ctime()
            

if __name__ == '__main__':
    main()    