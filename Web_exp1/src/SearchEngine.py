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
