import os
import json
from nltk.corpus import stopwords

DICT_PATH = "C:/Users/Administrator/Desktop/2020 FALL/Web/LAB/exp1/output/dict/"
OUTPUT_PATH = "C:/Users/Administrator/Desktop/2020 FALL/Web/LAB/exp1/output/full_dict/"
FULL_DICT = {}

def termStatistic(mail):
    fo = open(mail, 'r')
    readBuffer = fo.readlines()
    # count terms, ignore file address
    readBuffer = readBuffer[1::2]
    for index in range(len(readBuffer)):
        readBuffer[index] = readBuffer[index][:-1]
    for jsonItem in readBuffer:
        dictItem = json.loads(jsonItem)
        keys = dictItem.keys()
        for key in list(keys):
            if(FULL_DICT.__contains__(key)):
                FULL_DICT[key][0] = FULL_DICT[key][0] + dictItem[key]
                FULL_DICT[key][1] = FULL_DICT[key][1] + 1
            else:
                FULL_DICT[key] = [dictItem[key], 1]

if __name__ == '__main__':
    for root, dirs, files in os.walk(DICT_PATH):
        for fileName in files:
            print(fileName)
            termStatistic(root + '/' + fileName)
    STOPWORDS = stopwords.words('english')
    FULL_DICT = sorted(FULL_DICT.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    FILTERED_FULL_DICT = {}
    count = 0
    for words in FULL_DICT:
        if(words[0] not in STOPWORDS):
            FILTERED_FULL_DICT[words[0]] = words[1]
            count = count + 1
            if(count == 1000):
                break
    fo = open(OUTPUT_PATH + "full_dict.json", "a+", encoding='utf-8')
    full_dict_str = json.dumps(FILTERED_FULL_DICT)
    fo.write(full_dict_str)
    fo.write('\n')
    fo.close()
