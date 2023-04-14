# main program v2
# importing dependencies
from spellchecker import SpellChecker
from ocr import textRead
from nltk import *
from highLevel import spamDetect

spell = SpellChecker()


def analyse(imagePath):
    # severity variables
    wordSevMultiplier = 2.12  # how much to multiply the severity by if the raw is true
    useMultiplier = False  # whether to multiply the final score by the multiplier

    sevScoreWord = 0  # the severity score
    sevTotalWord = 0  # the total possible severity points for calculating percentage (temp)
    spamScoreSentences = 0
    spamTotalSentences = 0
    spellingMultiplier = 1.25
    wordScoreThreshold = 6  # percentage of misspelled words in order to trigger the spelling multiplier

    # LIST OF WORDS TO IGNORE
    ignorelist = ['www', 'http', 'https', 'http://', 'https://', 'com', 'co', 'uk']
    raw = textRead(imagePath, 'eng')  # get raw ocr
    rawList = [raw]
    if spamDetect(rawList) == 1:  # check if the entire message is spam
        useMultiplier = True
        print("TRUE AND TRUER")
    else:
        useMultiplier = False
        print("FALSE AND FALSER")

    rawString = " ".join(raw.split())
    textList = tokenize.sent_tokenize(rawString)  # split text into sentences which can be analysed.
    for i in textList:
        split = spell.split_words(i)  # split the list into words
        for x in split:
            correction = spell.correction(x)  # check word for spelling
            if x == correction and (4 < len(x)):  # if the correction is the same as the word (correctly spelled)
                sevTotalWord = sevTotalWord + 1
            elif correction is None and (len(x) > 4):
                # if cannot find an alternative spelling then assume it is a company name/technical term etc
                sevTotalWord = sevTotalWord + 1
            elif x in ignorelist and (len(x) > 4):
                # print(x, 'FLAGGED - Word in ignore list')
                sevTotalWord = sevTotalWord + 1
            else:
                if len(x) > 4:
                    # print true for condition misspelled
                    sevScoreWord = sevScoreWord + wordSevMultiplier
                    sevTotalWord = sevTotalWord + 1
                else:
                    sevTotalWord = sevTotalWord + 1

    for z in textList:
        z = [z]
        spamBool = spamDetect(z)  # boolean 1 for scam or 0 for not
        if spamBool == 1:
            spamScoreSentences = spamScoreSentences + 1
        spamTotalSentences = spamTotalSentences + 1
        print(z, spamBool)

    wordScore = (sevScoreWord / sevTotalWord) * 100
    spamSentencePercentage = (spamScoreSentences / spamTotalSentences) * 100
    print(wordScore)  # percentage of incorrect words
    print(spamSentencePercentage)

    if useMultiplier:  # if the entire message is flagged as spam, increase the score by the sev multiplier
        spamSentencePercentage = spamSentencePercentage * wordSevMultiplier

    if wordScore >= wordScoreThreshold:
        spamSentencePercentage = spamSentencePercentage + 1
        spamSentencePercentage = wordScore * spellingMultiplier  # if the misspelled words is over the
        # threshold,multiply the spamscore by the spellingmultiplier
    if wordScore <= wordScoreThreshold:
        spamSentencePercentage = spamSentencePercentage + (
                wordScore * 2)  # otherwise just add the misspelled percentage to the total (multiplied by two to
        # make it seem significant)

    if spamSentencePercentage >= 100:  # if the percentage is over 100 due to maths, set it to 100%
        spamSentencePercentage = 100

    print(sevTotalWord)  # totalwords
    print(sevScoreWord)  # total incorrect words


    print('Spam Score:', spamSentencePercentage)
    return spamSentencePercentage / 100  # return in decimal form for the javascript
