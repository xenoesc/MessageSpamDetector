#main program v2
#importing dependencies
from ocr import textRead
from spellchecker import SpellChecker
from nltk import *
from highLevel import spamDetect
####################
#IMPORTANT PREREQUISITE
#nltk must download punkt first, use the following:
#import nltk
#nltk.downloader('punkt')
####################
spell = SpellChecker() #declare spellcheck

#severity variables
sevPresets = [0.5,1] #the severity ratings [incorrectspelling, flaggedbymachinelearning]
wordSevMultiplier = 1 #how much severity to add per incorrect word


sevScoreWord = 0 #the severity score
sevTotalWord = 0 #the total possible severity points for calculating percentage (temp)
totalSeverity = 0

#LOCATION OF TEXT FILE
imagePath = 'tests/testemail1.png'
#LIST OF WORDS TO IGNORE
ignorelist = ['www','http','https','http://','https://','com','co','uk']

raw = textRead(imagePath, 'eng') #get raw ocr
rawString = " ".join(raw.split())
textList = tokenize.sent_tokenize(rawString)

def map_range(x, in_min, in_max, out_min, out_max): #mapping function to fix scale on the word severity score
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
#             inm.inM.outm.outM
map_scaler = [0.00, 100.00, 0.00, 800.00]

for i in textList:
    split = spell.split_words(i) #split the list into words
    for x in split:
       correction = spell.correction(x) #check word for spelling
       if(x==correction and (len(x) > 4)): #if the correction is the same as the word (correctly spelled)
           #print(x, 'CORRECT') #print false for condition misspelled DEBUG
           sevTotalWord = sevTotalWord + 1
       elif(correction==None and (len(x) > 4)):
           print(x, 'FLAGGED - Special Word') #if cannot find an alternative spelling then assume it is a company name/technical term etc
           sevTotalWord = sevTotalWord + 1
       elif(x in ignorelist and (len(x) > 4)):
           print(x, 'FLAGGED - Word in ignore list')
           sevTotalWord = sevTotalWord + 1
       else:
           if((len(x) > 4)):
               print(x,'INCORRECT','=>', correction) #print true for condition misspelled
               sevScoreWord = sevScoreWord + wordSevMultiplier
               sevTotalWord = sevTotalWord + 1
           else:
               sevTotalWord = sevTotalWord + 1

print('#####################################')
for z in textList:
    z=[z]
    spamBool = spamDetect(z) #boolean 1 for scam or 0 for not

    print(z, spamBool)

wordScore = (sevScoreWord/sevTotalWord)*100
print(sevTotalWord)
print(sevScoreWord)
print(wordScore)
wordScore_scaled = map_range(wordScore,map_scaler[0],map_scaler[1],map_scaler[2],map_scaler[3])
print(wordScore_scaled)