# Import Libraries
from stanfordcorenlp import StanfordCoreNLP
import json
import os
import re

nlp = StanfordCoreNLP(r'/Users/paulvidal/Documents/Nerd/stanford-corenlp-full-2018-10-05')

# Init variables
veryNegativeResults = 0
negativeResults = 0
neutralResults = 0
positiveResults = 0
veryPositiveResults = 0
invalidResults = 0

# Loop trough files and get the tweet

rootdir = '/Users/paulvidal/Documents/Nerd/NLP/tweets'
outputDirectory = '/Users/paulvidal/Documents/Nerd/NLP/results'
csvF = open(os.path.join(outputDirectory, 'list.csv'), "w+")
sentenceNumber = 1

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        f = open(os.path.join(subdir, file))
        rawTweet = f.read()
        for k in rawTweet.split("\n"):  
            sentence = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
            # print sentence
            # Sentiment 
            jsonSentiment = json.loads(nlp.annotate(sentence,
                                                    properties={
                                                        'annotators': 'sentiment',
                                                        'outputFormat': 'json'
                                                    }))
            
            currentSentence = ''        
            for s in jsonSentiment["sentences"]:
                for y in s["tokens"]:
                    currentSentence = currentSentence + ' ' +  y["originalText"]
                if(s["sentiment"] == "Verynegative"):
                    veryNegativeResults = veryNegativeResults + 1
                elif(s["sentiment"] == "Negative"):
                    negativeResults = negativeResults + 1
                elif(s["sentiment"] == "Neutral"):
                    neutralResults = neutralResults + 1
                elif(s["sentiment"] == "Positive"):
                    positiveResults = positiveResults + 1
                elif(s["sentiment"] == "Verypositive"):
                    veryPositiveResults = veryPositiveResults + 1
                else:
                    invalidResults = invalidResults + 1
            currentFilename = open(os.path.join(outputDirectory, 'analyzed-sentence-' + str(sentenceNumber) + '.txt'), "w+")
            currentFilename.write(currentSentence)
            currentFilename.close()
    
            csvF.write('analyzed-sentence-' + str(sentenceNumber) + '.txt' + ',' + s["sentiment"] + '\n')
            sentenceNumber = sentenceNumber + 1
            
        f.close()
    csvF.close()    



    

print "Very Negative Results:", veryNegativeResults
print "Negative Results:", negativeResults
print "Neutral Results:", neutralResults
print "Positive Results:", positiveResults
print "Very Positive Results:", veryPositiveResults
print "Invalid Results:", invalidResults
nlp.close()
 # Do not forget to close! The backend server will consume a lot memory.