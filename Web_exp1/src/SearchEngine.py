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
            print(fileName)
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
    returnDir.sort(key=lambda x:x[2], reverse=True)
    returnDir = returnDir[:10]
    FILE = []
    for returnFile in returnDir:
        FILE_CODE = str(returnFile[0]) + '_' + str(returnFile[1])
        FILE_ADDR = ADDR_MAPPING[FILE_CODE]
        FILE.append(FILE_ADDR)
        print(FILE_ADDR)

def calculateBool(termStack, operStack, operation):
    # calculate current result in the stack
    result = []
    if(operation == 'AND'):
        operRight = termStack.pop()
        operLeft = termStack.pop()
        for index in range(len(operLeft)):
            if(operLeft[index] != 0 and operRight[index] != 0):
                result.append(1)
            else:
                result.append(0)
    if(operation == 'OR'):
        operRight = termStack.pop()
        operLeft = termStack.pop()
        for index in range(len(operLeft)):
            if(operLeft[index] == 0 and operRight[index] == 0):
                result.append(0)
            else:
                result.append(1)
    if(operation == 'NOT'):
        oper = termStack.pop()
        for index in range(len(oper)):
            if(oper[index] == 0):
                result.append(1)
            else:
                result.append(0)
    termStack.append(result)
    if(len(operStack) > 0):
        if(operStack[-1] != '(' and operStack[-1] != ')'):
            # calculate until no operation required
            calculateBool(termStack, operStack, operStack.pop())

def SearchBool(inputStr):
    for root, dirs, files in os.walk(MATRIX_PATH):
        returnDir = []
        FILE = []
        for fileName in files:
            if(fileName == 'addr_mapping.json'):
                    continue
            print(fileName)
            fo = pd.read_csv(root + '/' + fileName)
            tfidfMat = np.array(fo)
            tfidfMat = np.delete(tfidfMat, 0, axis=1)
            query = inputStr.split(' ')
            termStack = []
            operStack = []
            for word in query:
                if(word == '('):
                    operStack.append(word)
                if(word == ')'):
                    # pop ')' and '('
                    operStack.pop()
                    operStack.pop()
                    if(operStack[-1] == 'AND' or operStack[-1] == 'OR' or operStack[-1] == 'NOT'):
                        calculateBool(termStack, operStack, operStack.pop())
                if(word == 'AND' or word == 'OR' or word == 'NOT'):
                    operStack.append(word)
                else:
                    termStack.append(list(tfidfMat[KEYS.index(word)]))
                    # push vec, if we have operation waiting then do calculation
                    if(len(operStack) > 0):
                        if(operStack[-1] == 'AND' or operStack[-1] == 'OR' or operStack[-1] == 'NOT'):
                            calculateBool(termStack, operStack, operStack.pop())
            MAT_FILE_NUM = int(fileName.split('_')[2].split('.')[0])
            boolVec = termStack.pop()
            for index in range(len(boolVec)):
                if(boolVec[index] == 1):
                    returnDir.append((MAT_FILE_NUM ,index))
        for returnFile in returnDir:
            FILE_CODE = str(returnFile[0]) + '_' + str(returnFile[1])
            FILE_ADDR = ADDR_MAPPING[FILE_CODE]
            FILE.append(FILE_ADDR)
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
    confirmButtomTFIDF = tkinter.Button(window, text='SearchTFIDF', command=lambda : SearchTFIDF(searchWords.get()))
    confirmButtomTFIDF.pack()
    confirmButtomBOOL = tkinter.Button(window, text='SearchBool', command=lambda : SearchBool(searchWords.get()))
    confirmButtomBOOL.pack()
    window.mainloop()
