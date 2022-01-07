# @author Tianle Chen, tc822; Yuchen Zhao, yz1116
import re
import math


def clean(reader):
    reader = reader.lower()
    reader = re.sub(r'\bhttp[s]://.*?\s\b', '', reader)
    reader = re.sub(r'\s+', ' ', reader)
    data = re.sub(r'[^\w\s]', '', reader)

    return data


# print(clean())


def remove(data):
    with open('stopwords.txt') as stopwords:
        reader = stopwords.readlines()
        for words in reader:
            data = ' '.join([word for word in data.split(' ') if word != words.strip()])
    return data


# print(remove())


def stemming(original):
    result = re.sub(r'ing|ly|ment', '', original)
    return result


# print(stemming())


def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict


def computeIDF(documents):
    N = len(documents)
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    for word, val in idfDict.items():
        if val != 0:
            idfDict[word] = math.log(N / float(val)) + 1
        else:
            idfDict[word] = 0
    return idfDict


def computeTFIDF(tfBagOfWords, idf):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = round(val * idf[word], 2)
    return tfidf


def textProc():
    word_dict = {}
    with open('tfidf_docs.txt') as f:
        files = f.readlines()
        for filename in files:
            with open('preproc_' + filename.strip(), 'w') as outfile:
                with open(filename.strip()) as file:
                    reader = file.read()
                    result = stemming(remove(clean(reader)))
                    print(result, file=outfile)
                    wordlist = result.split()
                    for word in wordlist:
                        if word not in word_dict:
                            word_dict[word] = 0
    return word_dict


# print((textProc()))


def get_Idf():
    documents = []
    with open('tfidf_docs.txt') as f:
        files = f.readlines()
        for filename in files:
            with open(filename.strip()) as file:
                reader = file.read()
                result = stemming(remove(clean(reader)))
                numOfWords = textProc()
                for word in result.split():
                    numOfWords[word] += 1
            documents.append(numOfWords)
    return computeIDF(documents)


# print(get_Idf())


def get_tf_idf():
    with open('tfidf_docs.txt') as f:
        files = f.readlines()
        for filename in files:
            with open('tfidf_' + filename.strip(), 'w') as outfile:
                with open(filename.strip()) as file:
                    reader = file.read()
                    result = stemming(remove(clean(reader)))
                    numOfWords = textProc()
                    for word in result.split():
                        numOfWords[word] += 1
                    tf = computeTF(numOfWords, result.split())
                    tfidf = computeTFIDF(tf, get_Idf())
                    st = dict(sorted(tfidf.items(), key=lambda x: (-x[1], x[0])))
                    lst = dict([i for i in st.items()][:5])
                print(lst, file=outfile)


get_tf_idf()
