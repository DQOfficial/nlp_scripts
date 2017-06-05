# sentiment analyzer
# calculates subjectivity and polarity and returns the original string

from textblob import TextBlob
import numpy as np
import pandas as pd

# change file name below:
file = 'eq_10.txt'

responses = open(file, 'rb').read().decode('utf-8').splitlines()

my_list = []

for response in responses:
    my_list.append(TextBlob(response))

responses = my_list

response_list = []
subj_list = []
pol_list = []
sent_list = []

for response in responses:
    response_list.append(response)
    subj_list.append(response.sentiment.subjectivity)
    pol_list.append(response.sentiment.polarity)
    sent_list.append(response.sentiment)

# now let's create a dataframe with all of these lists for easy excel export
export_df = pd.DataFrame({'response':response_list,
                          'subjectivity':subj_list,
                          'polarity':pol_list})
#print(export_df.head())
#print(response_list[:5])
# print("The average sentiment score is:", np.round(np.mean(pol_list),3))
# print("The average subjectivity score is:", np.round(np.mean(subj_list),3))
#export_df.to_csv('External Question 10 Sentiment Score.csv')

# next, let's read in the list of top words and compute the sentiment on
# responses containing key words
df = pd.read_csv('External Question 10 Answers.csv')
