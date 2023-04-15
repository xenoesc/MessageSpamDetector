# main program v2
# importing dependencies
from spellchecker import SpellChecker
from ocr import textRead
from nltk import *
from highLevel import spamDetect

spell = SpellChecker()


def analyse(imagePath):
    # severity variables
    allSpam = False  # whether the entire message is spam, aside from the individual sentences
    badWords = 0  # the number of misspelled words
    totalWords = 0  # the total words
    spamSentences = 0  # the number of sentences flagged as spam.
    totalSentences = 0  # the total number of sentences
    wordScoreThreshold = 5  # percentage of misspelled words in order to be significant
    badWordMultiplier = 1.12

    wordPercentage = 0
    sentencePercentage = 0
    spamTotal = 0

    # LIST OF WORDS TO IGNORE
    ignorelist = ['www', 'http', 'https', 'http://', 'https://', 'com', 'co', 'uk']
    raw = textRead(imagePath, 'eng')  # get raw ocr
    rawList = [raw]
    if spamDetect(rawList) == 1:  # check if the entire message is spam
        useMultiplier = True
    else:
        useMultiplier = False

    rawString = " ".join(raw.split())
    textList = tokenize.sent_tokenize(rawString)  # split text into sentences which can be analysed.
    for i in textList:
        split = spell.split_words(i)  # split the list into words
        for x in split:
            correction = spell.correction(x)  # check word for spelling
            if x == correction and (4 < len(x)):  # if the correction is the same as the word (correctly spelled)
                totalWords = totalWords + 1
            elif correction is None and (len(x) > 4):
                # if cannot find an alternative spelling then assume it is a company name/technical term etc
                totalWords = totalWords + 1
            elif x in ignorelist and (len(x) > 4):
                # print(x, 'FLAGGED - Word in ignore list')
                totalWords = totalWords + 1
            else:
                if len(x) > 4:
                    # print true for condition misspelled
                    badWords = badWords + 1  # increase the bad words
                    totalWords = totalWords + 1
                else:
                    totalWords = totalWords + 1

    for z in textList:
        z = [z]
        spamBool = spamDetect(z)  # boolean 1 for scam or 0 for not
        if spamBool == 1:
            spamSentences = spamSentences + 1

        totalSentences = totalSentences + 1
        print(z, spamBool)

    if totalWords!=0 and totalSentences!=0:
        wordPercentage = (badWords / totalWords) * 100
        sentencePercentage = (spamSentences / totalSentences) * 100
    else:
        return 0

    print("Word Percentage: ", wordPercentage)
    print("Sentence Percentage: ", sentencePercentage)

    spamTotal = sentencePercentage

    if sentencePercentage >= 100:  # if all the sentences trigger spam, then check for spelling
        if wordPercentage <= wordScoreThreshold:
            spamTotal = spamTotal - wordPercentage
        else:
            round(spamTotal) # round the total to make sure the percentage is accurate

            spamTotal = spamTotal / 100  # convert to decimal
            print("SpamTotal1: ", spamTotal)
            return spamTotal

    else:
        if useMultiplier:
            if sentencePercentage <= 50:
                spamTotal = spamTotal + 25  # if the sentence percentage is low and useMultiplier is true, then increase the total score by more
            else:
                spamTotal = spamTotal + 10

        if spamTotal >= 100: # check if the score is above 100, if so, then set it to 100 as the webpage needs values to be within the range of 100.
            spamTotal = 100

        if wordPercentage >= wordScoreThreshold:
            spamTotal = spamTotal * badWordMultiplier  # if there is a significant amount of misspelled words, multiply the total score by the multiplier
        else:
            spamTotal = spamTotal - wordPercentage

        round(spamTotal) # round the total to make sure the percentage is accurate

        spamTotal = spamTotal / 100  # convert to decimal
        print("SpamTotal2: ", spamTotal)
        return spamTotal
