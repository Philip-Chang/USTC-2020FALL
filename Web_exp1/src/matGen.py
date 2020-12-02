import os
import json
import numpy as np
import pandas as pd

DICT_PATH = "D:/Users/Desktop/Web/exp1/output/full_dict/"
MAIL_PATH = "D:/Users/Desktop/Web/exp1/output/dict/"
MATRIX_PATH = "D:/Users/Desktop/Web/exp1/output/matrix/"
FULL_DICT = {}

TOTAL_FILE_NUM = 517401
MAX_MAT_SIZE = 50000
MAT_INDEX = 0
MAT_FILE_NUM = 0
TMP_NUM = 0

TFIDF = np.zeros((1000, MAX_MAT_SIZE))
FILE_ADDR_MAPPING = {}

def matGen(fileName, keys):
    # for monitoring usage
    global TMP_NUM
    TMP_NUM = TMP_NUM + 1
    print(str(TMP_NUM) + '/150: ' + fileName)
    global MAT_INDEX
    global MAX_MAT_SIZE
    global MAT_FILE_NUM
    fo = open(fileName, 'r')
    readBuffer = fo.readlines()
    fo.close()
    # fileList contains FILE_NUM and Address
    fileList = readBuffer[::2]
    for index in range(len(fileList)):
        fileList[index] = json.loads(fileList[index][:-1])
    # itemList contains lexical terms
    itemList = readBuffer[1::2]
    for index in range(len(itemList)):
        itemList[index] = json.loads(itemList[index][:-1])
    # calculate tf-idf vector for each document
    for index in range(len(fileList)):
        # one document
        FILENUM = list(fileList[index].keys())[0]
        terms = itemList[index]
        for keyIndex in range(len(keys)):
            # for every key in dictionary
            if(terms.__contains__(keys[keyIndex])):
                tf = 1 + np.log(terms[keys[keyIndex]]) / np.log(10)
                TFIDF[keyIndex][MAT_INDEX] = tf * FULL_DICT[keys[keyIndex]][1]
            else:
                TFIDF[keyIndex][MAT_INDEX] = 0
        # add new mapping to mapping dictionary
        FILE_ADDR_MAPPING[str(MAT_FILE_NUM) + '_' + str(MAT_INDEX)] = fileList[index][FILENUM]
        MAT_INDEX = MAT_INDEX + 1
        if(MAT_INDEX == MAX_MAT_SIZE):
            # if buffer reaches maximum then write file
            pd_data = pd.DataFrame(TFIDF, index=keys)
            pd_data.to_csv(MATRIX_PATH + 'tfidf_matrix_' + str(MAT_FILE_NUM) + '.csv')
            MAT_INDEX = 0
            # fo = open(MATRIX_PATH + 'tfidf_matrix_' + str(MAT_FILE_NUM) + '.json', 'a+', encoding='utf-8')
            # TFIDF_str = json.dumps(TFIDF.tolist())
            # fo.write(TFIDF_str)
            # fo.close()
            MAT_FILE_NUM = MAT_FILE_NUM + 1


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
            matGen(root + '/' + fileName, list(keys))
    # write remaining tf-idf
    pd_data = pd.DataFrame(TFIDF, index=keys)
    pd_data.to_csv(MATRIX_PATH + 'tfidf_matrix_' + str(MAT_FILE_NUM) + '.csv')
    # write mapping file
    fo = open(MATRIX_PATH + 'addr_mapping.json', 'a+', encoding='utf-8')
    MAPPING_STR = json.dumps(FILE_ADDR_MAPPING)
    fo.write(MAPPING_STR)
    fo.close()
