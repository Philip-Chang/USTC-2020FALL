import os
import json
import numpy as np

DICT_PATH = "C:/Users/Administrator/Desktop/2020 FALL/Web/LAB/exp1/output/full_dict/"
MAIL_PATH = "C:/Users/Administrator/Desktop/2020 FALL/Web/LAB/exp1/output/dict/"
FULL_DICT = {}
TOTAL_FILE_NUM = 517401
TFIDF = np.zeros((1000, TOTAL_FILE_NUM))

def matGen(fileName, keys):
    fo = open(fileName, 'r')
    readBuffer = fo.readlines()
    # fileList contains FILE_NUM and Address
    fileList = readBuffer[::2]
    for File in fileList:
        File = File[:-1]
        File = json.loads(File)
    # itemList contains lexical terms
    itemList = readBuffer[1::2]
    for Item in itemList:
        Item = Item[:-1]
        Item = json.loads(Item)
    for index in range(len(fileList)):
        FILENUM = int(fileList[index].keys()[0])
        terms = itemList[index]
        for keyIndex in range(len(keys)):
            if(terms.__contains__(keys[keyIndex])):
                tf = 1 + np.log(terms[keys[keyIndex]]) / np.log(10)
                TFIDF[keyIndex][FILENUM - 1] = tf * FULL_DICT[keys[keyIndex]][1]
            else:
                TFIDF[keyIndex][FILENUM - 1] = 0

if __name__ == '__main__':
    fo = open(DICT_PATH + 'full_dict.json', 'r')
    readBuffer = fo.readlines()
    FULL_DICT = json.loads(readBuffer[0])
    keys = FULL_DICT.keys()
    for key in keys:
        # calculate idf for every item
        FULL_DICT[key][1] = np.log(TOTAL_FILE_NUM / FULL_DICT[key][1]) / np.log(10)
    fo.close()
    for root, dirs, files in os.walk(MAIL_PATH):
        for fileName in files:
            matGen(root + '/' + fileName, keys)
