import json
import sys
from transformers import pipeline
import pandas as pd


def headline_analyzer(text):
  # word count and character count
  characters = len(text)
  words = len(text.split())

  if (words != 0):
      
        # using a pretrained model for the sentiment analysis
        classifier = pipeline('sentiment-analysis')
        sentiment=classifier(text)
        sentiment = sentiment[0]['label']

        # calling in the datasets
        common_words = pd.read_csv("./csv_folder/common_words.csv")
        intelligent_words = pd.read_csv("./csv_folder/intelligent_words1.csv")
        sensory_words = pd.read_csv("./csv_folder/sensory_words.csv")
        spam_words = pd.read_csv("./csv_folder/spam_words.csv")
        spiritual_words = pd.read_csv("./csv_folder/spritual_words.csv")
        emotional_words = pd.read_csv("./csv_folder/emotional_words1.csv", names=['try'],encoding='cp1252')

        uncommon_words = pd.read_csv("./csv_folder/uncommon_words.csv", names=['try'])
        uncommon_words = uncommon_words[0:]
        power_words = pd.read_csv("./csv_folder/power_words.csv", names=['try'])
        power_words = power_words[0:]

        # calculating percentages

        percentages = []
        for i in [common_words,intelligent_words,sensory_words,spiritual_words,uncommon_words,power_words, emotional_words, spam_words]:
            word_list = i['try'].str.lower().str.strip().tolist()
            headline_list = text.lower().split()

            intersection = set(headline_list)&set(word_list)
            sim_length = len(intersection)
            percentage = (sim_length/words) * 100
            
            percentages.append(int(percentage))
            percentages.append(intersection)

        
        common_perc, common_list, intelligent_perc, intelligent_list ,sensory_perc, sensory_list,spiritual_perc, spiritual_list,uncommon_perc, uncommon_list,power_perc, power_list,emotional_perc, emotional_list, spam_perc, spam_list = percentages

        # EMOTIONAL MARKETING VALUE
        emv = {"intelligence":intelligent_perc,"emotion":emotional_perc,"sprit":spiritual_perc}
        max_key = max(emv, key=emv.get)
        max_value = emv[max_key]

        # word balance (used this article https://coschedule.com/blog/how-to-write-the-best-headlines-that-will-increase-traffic#review)
        if (power_perc > 0) & ((emotional_perc >= 10) & (emotional_perc <= 15)) & ((uncommon_perc >=10) & (uncommon_perc<=20)) & ((common_perc >=20) & (common_perc<=30)):
            word_balance = "Perfect!"
        else:
            word_balance = "Can Improve"

        # Overall Score
        overall = 0
        recommendation = []
        if power_perc > 0:
            overall += 20
        else:
          recommendation.append("Add a few Power Words")
        if emotional_perc >= 10:
            overall += 20
        else:
          recommendation.append("Add some Emotional Words")
        if common_perc >=20:
            overall +=20
        else:
          recommendation.append("Add some Common Words")
        if (words >= 5 and words <=7):
            overall += 20
        else:
          recommendation.append("Using between 5 - 7 words is ideal")
        if characters <= 57:
            overall += 20
        else:
          recommendation.append("Having more than 57 characters is not ideal")

  else:
      print("Input your headline")
    
  

  return recommendation, overall, common_perc, common_list, uncommon_perc, uncommon_list, power_perc, power_list, intelligent_perc, intelligent_list ,sensory_perc, sensory_list,spiritual_perc, spiritual_list, emotional_perc, emotional_list, max_key, max_value, words, characters, word_balance, sentiment, spam_perc, spam_list
if __name__ == "__main__":
    text = str(input())
    recommendation, overall, common_perc, common_list, uncommon_perc, uncommon_list, power_perc, power_list, intelligent_perc, intelligent_list ,sensory_perc, sensory_list,spiritual_perc, spiritual_list,emotional_perc, emotional_list,max_key, max_value, words, characters,word_balance, sentiment, spam_perc, spam_list = headline_analyzer(text)
    entry = {
        "Overall Score": overall,
        "Recommendation": list(recommendation),
        "Headline Length": f"{characters} characters",
        "Word Count": f"{words} words",
        "Common Words %": f"{common_perc} %",
        "Common Words": list(common_list),
        "Uncommon Words %": f"{uncommon_perc} %",
        "Uncommon Words": list(uncommon_list),
        "Power Words %": f"{power_perc} %",
        "Power Words": list(power_list),
        "Intelligent Words %": f"{intelligent_perc} %",
        "Intelligent Words": list(intelligent_list),
        "Spiritual Words %": f"{spiritual_perc} %",
        "Spiritual Words": list(spiritual_list),
        "Emotional Words %": f"{emotional_perc} %",
        "Emotional Words": list(emotional_list),
        "Sensory Words %": f"{sensory_perc} %",
        "Sensory Words": list(sensory_list),
        "Word Balance": word_balance,
        "Sentiment": sentiment,
        "EMV_key": max_key,
        "EMV_value": max_value,
        "Spam Words": list(spam_list), 
        "Spam Percentage": f"{spam_perc} %"
       
    }

    print(json.dumps(entry))