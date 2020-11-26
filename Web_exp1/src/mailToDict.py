import os
import re
import json
import nltk
import numpy as np

PATH = "../dataset/enron_mail_20150507/maildir/"
DICT_PATH = "../output/dict/"
FILE_NUM = 0
FILE_CAN_NOT_DECODE = 0

def countToken(token_list, file_addr, subdir):
    # count lexical items and store in a dictionary
    token_dict = {}
    for token in token_list:
        if(token_dict.__contains__(token)):
            token_dict[token] = token_dict[token] + 1
        else:
            token_dict[token] = 1
    #tokenProcess(token_dict, file_num)
    token_dict_str = json.dumps(token_dict)
    file_addr_str = json.dumps(file_addr)
    dictFile = open(DICT_PATH + subdir + '_dict.json', "a+", encoding='utf-8')
    dictFile.write(file_addr_str)
    dictFile.write('\n')
    dictFile.write(token_dict_str)
    dictFile.write('\n')
    dictFile.close()
    return token_dict

def mailPerProcess(mail, subdir):
    # Precess email and sent tokenized items to countToken()
    global FILE_CAN_NOT_DECODE
    global FILE_NUM
    fo = open(mail, "r")
    try:
        contexts = fo.readlines()
        bodyStart = 0
        bodyEnd = 0
        for index in range(len(contexts)):
            # first blank line as body starts
            if(bodyStart == 0):
                if(contexts[index] == '\n'):
                    bodyStart = index
            # end of file or '-----' as body ends
            if(re.match("-----", contexts[index])):
                bodyEnd = index
        if(bodyEnd == 0):
            bodyEnd = len(contexts) - 1
        # extract body part and do perprocess
        if(bodyStart != bodyEnd):
            mailBody = contexts[bodyStart : bodyEnd]
            mailBody.append(contexts[bodyEnd])
            tokens = []
            for sentence in mailBody:
                tokens.append(nltk.word_tokenize(sentence))
            # erase capital letters and remove none-letter/number characters
            for token_index in range(len(tokens)):
                token_tmp = []
                for index in range(len(tokens[token_index])):
                    if(re.search(r'\w', tokens[token_index][index]) is not None):
                        tokens[token_index][index] = tokens[token_index][index].lower()
                        token_tmp.append(tokens[token_index][index])
                tokens[token_index] = token_tmp[:]
            # root
            lemmatizer = nltk.stem.WordNetLemmatizer()
            root_tokens = []
            for token in tokens:
                if(token):
                    root_tokens.append([lemmatizer.lemmatize(x) for x in token])
            mailDict = countToken(sum(root_tokens, []), {FILE_NUM: mail}, subdir)
            FILE_NUM = FILE_NUM + 1
    except UnicodeDecodeError:
        FILE_CAN_NOT_DECODE = FILE_CAN_NOT_DECODE + 1
        print("Decode Error: " + mail)
        return None
    fo.close()
    return mailDict

def spanDir(path, subdir):
    print(path)
    global FILE_NUM
    for root, dirs, files in os.walk(path, topdown=False):
        for fileName in files:
            mailPerProcess(root + '/' + fileName, subdir)

if __name__ == '__main__':
    subDirList = os.listdir(PATH)
    for subdir in subDirList:
        spanDir(PATH + subdir + '/', subdir)
    print("Total Processed File Num: " + str(FILE_NUM))
