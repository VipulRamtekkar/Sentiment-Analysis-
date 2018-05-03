
import nltk as nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
from tweepy import OAuthHandler
import csv
import re
import string

# The keys are generated using twitter app development 

ckey = "NQQxj9dYUeOti4IBS6CUIIEpK"
csecret = "JfPX808qem2uiPMIyk6tWL4Dt9NReqN3f5HCGAaFeLwFLQvC1d"
atoken = "3459698352-T7P45jHgL13aoxeseW792Tj4cPoH97C97Sy5tcp"
asecret = "7eSHpqvlyhratjdL6slTN6ppQyb92k4BMjaIat8y3dram"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

analyzer = SentimentIntensityAnalyzer()

csvFile = open('result1.csv', 'a')

summ = 0
average = 0
followers = 0

for tweet in tweepy.Cursor(api.search,
                           q="oneplus6",  # topic we want to search for
                           count=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en",
                           since='2018-04-27',  # day we want to search for
                           until='2018-04-28').items():

    csvWriter = csv.writer(csvFile,)
    #x = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text.encode('utf-8')).split())
    x = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())

    if x[:2] != "RT":

        if float(analyzer.polarity_scores(x)["compound"]) != 0:
            summ = summ + float(analyzer.polarity_scores(x)["compound"]) * tweet.user.followers_count
            followers = followers + tweet.user.followers_count

        if followers != 0:
            average = summ / followers

        csvWriter.writerow([analyzer.polarity_scores(x)["compound"], x, tweet.created_at, average, tweet.user.followers_count])
        print(x)

    else:
        continue


print(average)
print(followers)
csvFile.close()
