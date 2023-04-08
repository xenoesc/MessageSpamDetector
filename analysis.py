#main program v2
#importing dependencies
from spellchecker import SpellChecker
from ocr import textRead
from nltk import *
from highLevel import spamDetect
####################
#IMPORTANT PREREQUISITE
#nltk must download punkt first, use the following:
#import nltk
#nltk.downloader('punkt')
####################

spell = SpellChecker()



def analyse(imagePath):
    # severity variables
    map_scaler = [0.00, 100.00, 0.00, 800.00]
    wordSevMultiplier = 1.5  # how much to multiply the severity by if the raw is true
    useMultiplier = False #whether or not to multiply the final score by the multiplier

    sevScoreWord = 0  # the severity score
    sevTotalWord = 0  # the total possible severity points for calculating percentage (temp)
    totalSeverity = 0
    spamScoreSentences = 0
    spamTotalSentences = 0

    # LIST OF WORDS TO IGNORE
    ignorelist = ['www', 'http', 'https', 'http://', 'https://', 'com', 'co', 'uk']
    raw = textRead(imagePath, 'eng')  # get raw ocr

    if(spamDetect(raw) == 1): #check if the entire message is spam
        useMultiplier=True
    else:
        useMultiplier = False


    rawString = " ".join(raw.split())
    textList = tokenize.sent_tokenize(rawString) #split text into sentences which can be analysed.
    for i in textList:
        split = spell.split_words(i) #split the list into words
        for x in split:
           correction = spell.correction(x) #check word for spelling
           if(x==correction and (len(x) > 4)): #if the correction is the same as the word (correctly spelled)
               #print(x, 'CORRECT') #print false for condition misspelled DEBUG
               sevTotalWord = sevTotalWord + 1
           elif(correction==None and (len(x) > 4)):
               #print(x, 'FLAGGED - Special Word') #if cannot find an alternative spelling then assume it is a company name/technical term etc
               sevTotalWord = sevTotalWord + 1
           elif(x in ignorelist and (len(x) > 4)):
               #print(x, 'FLAGGED - Word in ignore list')
               sevTotalWord = sevTotalWord + 1
           else:
               if((len(x) > 4)):
                   #print(x,'INCORRECT','=>', correction) #print true for condition misspelled
                   sevScoreWord = sevScoreWord + wordSevMultiplier
                   sevTotalWord = sevTotalWord + 1
               else:
                   sevTotalWord = sevTotalWord + 1

    #print('#####################################')
    for z in textList:
        z=[z]
        spamBool = spamDetect(z) #boolean 1 for scam or 0 for not
        if (spamBool == 1):
            spamScoreSentences = spamScoreSentences + 1
        spamTotalSentences = spamTotalSentences + 1
        print(z, spamBool)


    wordScore = (sevScoreWord/sevTotalWord)*100
    spamSentencePercentage = (spamScoreSentences / spamTotalSentences) * 100
    if(useMultiplier == True):
        spamSentencePercentage = spamSentencePercentage * wordSevMultiplier
    if(spamSentencePercentage >= 100):
        spamSentencePercentage = 100

    spamTotal = (wordScore + spamSentencePercentage)/2


    #print(sevTotalWord) #totalwords
    #print(sevScoreWord) #total incorrect wprds
    #print(wordScore) #percentage of incorrect words




    #print('Wordscore:',wordScore_scaled)
    #print('Spam Score:',spamSentencePercentage)
    #print('Total Score:',spamTotal)
    return((spamTotal)/100)


