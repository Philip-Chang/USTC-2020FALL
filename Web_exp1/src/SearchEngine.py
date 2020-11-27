import os
import json
import numpy as np
import pandas as pd
import tkinter

MATRIX_PATH = "D:/Users/Desktop/Web/exp1/output/matrix/"
DICT_FILE = "D:/Users/Desktop/Web/exp1/output/full_dict/full_dict.json"
MAPPING_FILE = "D:/Users/Desktop/Web/exp1/output/matrix/addr_mapping.json"
ADDR_MAPPING = {}
FULL_DICT = {}
KEYS = []
TOTAL_FILE_NUM = 517401

def SearchTFIDF(inputStr):
    global TOTAL_FILE_NUM
    keyWords = inputStr.split(',')
    searchVec = []
    for key in KEYS:
        if(key in keyWords):
            FULL_DICT[key][1] = np.log(TOTAL_FILE_NUM / FULL_DICT[key][1]) / np.log(10)
            searchVec.append(FULL_DICT[key][1])
        else:
            searchVec.append(0)
    searchVec = np.array(searchVec)
    returnDir = []
    for root, dirs, files in os.walk(MATRIX_PATH):
        for fileName in files:
            if(fileName == 'addr_mapping.json'):
                continue
            fo = pd.read_csv(root + '/' + fileName)
            tfidfMat = np.array(fo)
            # drop term index, each row is tf-idf vec of a file
            tfidfMat = (tfidfMat.T)[1:]
            MAT_FILE_NUM = int(fileName.split('_')[2].split('.')[0])
            for MAT_INDEX in range(len(tfidfMat)):
                if(np.dot(tfidfMat[MAT_INDEX], tfidfMat[MAT_INDEX]) == 0):
                    continue
                mode_tmp = (np.dot(searchVec, searchVec) * np.dot(tfidfMat[MAT_INDEX], tfidfMat[MAT_INDEX]))**0.5
                correlation = np.dot(searchVec, tfidfMat[MAT_INDEX]) / mode_tmp
                if(correlation > 0):
                    returnDir.append((MAT_FILE_NUM, MAT_INDEX, correlation))
            break
    returnDir.sort(key=lambda x:x[2], reverse=True)
    for returnFile in returnDir:
        FILE_CODE = str(returnFile[0]) + '_' + str(returnFile[1])
        FILE_ADDR = ADDR_MAPPING[FILE_CODE]
        print(FILE_ADDR)
    

if __name__ == '__main__':
    fo = open(MAPPING_FILE, 'r')
    readBuffer = fo.readline()
    fo.close()
    ADDR_MAPPING = json.loads(readBuffer)
    # print(list(ADDR_MAPPING.keys())[len(list(ADDR_MAPPING.keys())) - 1])
    fo = open(DICT_FILE, 'r')
    dictBuffer = fo.readline()
    fo.close()
    FULL_DICT = json.loads(dictBuffer)
    KEYS = list(FULL_DICT.keys())
    # print(KEYS[-1])
    window = tkinter.Tk()
    searchWords = tkinter.Entry(window, bd=5)
    searchWords.pack()
    confirmButtom = tkinter.Button(window, text='Search', command=lambda : SearchTFIDF(searchWords.get()))
    # confirmButtom = tkinter.Button(window, text='Search', command=lambda : SearchTFIDF('nothing,please'))
    confirmButtom.pack()
    window.mainloop()
