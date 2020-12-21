# Huffman Encoding
# Author: Vladyslav Dyshkant

import math

def frequencies(s=''):
    temp = list(dict.fromkeys(s))
    result = []
    if len(s) > 1:
        for i in temp:
            result.append((i, s.count(i)))
        swapped = True
        while swapped:
            swapped = False
            for i in range(len(result) - 1):
                if result[i][1] < result[i + 1][1]:
                    result[i], result[i + 1] = result[i + 1], result[i]
                    swapped = True
        return result if len(result) > 1 else print('Please enter more than one type of symbol')
    else:
        print('Please enter more than one character')

def encoding_dictionary(freqs=[]):
    if freqs is not None:
        if len(freqs) > 1:
            result = dict.fromkeys([i[0] for i in freqs], '')
            freqs = freqs.copy()
            try:
                countOfDigits = math.log(len(freqs) - 1, 2)
            finally:
                if len(freqs) == 0:
                    countOfDigits = 1
            digitsAll = ''
            digitsLeft = ''
            if countOfDigits.is_integer(): # if length of freqs is power of two
                digitsAll = int(countOfDigits) + 1 # count of 0 or 1 for tree encoding
            else: # if length of freqs is not power of two
                digitsLeft = int(countOfDigits) + 1 # count of 0 or 1 for left side tree encoding with
                                                    # greater frequencies
                digitsRight = int(math.ceil(countOfDigits)) + 1 # count of 0 or 1 for right side tree
                                                                # encoding with less frequencies
                countForLess = int(math.pow(2, digitsLeft) - (len(freqs) - 1)) # count of elements for
                                                                               # left side of tree
            condition = False
            switchToNext = False
            counter = 0
            for i in result:
                if counter == 0:
                    result[i] = '0'
                    if digitsAll:
                        counter = 1
                    elif digitsLeft:
                        counter = 2
                    continue
                if counter == 2:
                    if not switchToNext:
                        if not condition:
                            result[i] = bin(int('1' + '0' * (digitsLeft - 1), 2))[2:]
                            temp = result[i]
                            countForLess -= 1
                            condition = True
                        else:
                            result[i] = bin(int(temp, 2) + 1)[2:]
                            temp = result[i]
                            countForLess -= 1
                        if countForLess == 0:
                            switchToNext = True
                            condition = False
                    else:
                        if not condition:
                            tmp = -1 if int(math.pow(2, digitsLeft) - (len(freqs) - 1)) % 2 == 1 else -2
                            result[i] = bin(int(temp[:tmp] + '1' + '0' * (digitsRight - len(temp[:tmp] + '1')), 2))[2:]
                            del tmp
                            temp = result[i]
                            condition = True
                        else:
                            result[i] = bin(int(temp, 2) + 1)[2:]
                            temp = result[i]
                if counter == 1:
                    if not switchToNext:
                        result[i] = bin(int('1' + '0' * (digitsAll - 1), 2))[2:]
                        temp = result[i]
                        switchToNext = True
                    else:
                        result[i] = bin(int(temp, 2) + 1)[2:]
                        temp = result[i]
            return result

def encode(freqs=[], s=''):
    if len(freqs) > 1:
        freqs = freqs.copy()
        string = s
        encoding = encoding_dictionary(freqs)
        result = ''
        for i in string:
            result += encoding[i]
        return result

def decode(freqs=[], bits=''):
    if len(freqs) > 1:
        freqs = freqs.copy()
        encoding = encoding_dictionary(freqs)
        decoding = dict()
        result = ""
        for i in encoding:
            decoding[encoding[i]] = i
        str = ''
        for i in range(len(bits)):
            str += bits[i]
            if str in decoding:
                result += decoding[str]
                str = ''
        return result

validString = False
while not validString:
    string = input("Input your text: ")
    freqs = frequencies(string)

    if freqs:
        validString = True
        print("Frequency:", end=' ')
        print(freqs)
        print("Dictionary of encoding:", end=' ')
        encodingDict = encoding_dictionary(freqs)
        print(encodingDict)

        encoding = encode(freqs, string)
        decoding = decode(freqs, encoding)

        print("Encoding:", end=' ')
        print(encoding)
        print("Decoding:", end=' ')
        print(decoding)

        if string == decoding:
            stringLen = len(string) * 8
            encodingLen = len(encoding)
            print("Memory before compression:", end=' ')
            print(stringLen, " bits")
            print("Memory after compression:", end=' ')
            print(encodingLen, " bits")
            print("Save memory:", end=' ')
            print(stringLen - encodingLen, " bits")
            print("Succeed")
        else:
            print("Unsucceed")