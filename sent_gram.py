import pandas as pd
from textblob import TextBlob
import numpy as np

# run the script on each question and write out the output files
esr_q7 = 'text_files/esr_q7.txt'
esrm_q5 = 'text_files/esrm_q5.txt'
isr_q5 = 'text_files/isr_q5.txt'

def convert_response(file):
    responses = open(file, 'rb').read().decode('utf-8').splitlines()
    return responses


def calc_ngram(file,N):
    # read in file
    responses = open(file, 'rb').read().decode('utf-8').splitlines()

    response_list = []

    # convert all words to lower case and remove punctuation
    for response in responses:
        response = str.lower(response).split(' ')
        response_list.append(response)

    punctuation = [',',';','.',':','?','!',"'",'"','...',"''",'-','`','``','(',')']
    no_puncs = []

    # append the no punctuation strings to a new list
    for w in response_list: # was response_list
        if w not in punctuation:
            no_puncs.append(w)

    response_list = no_puncs

# def calc_ngram(response_list,N):
    my_list = []

    for response in response_list:  # in each response
        for i in range(len(response)):  # in each word
            if len(response[i:i + N]) == N:  # throw out the ones that aren't N words long
                my_list.append(response[i:i + N])

    joined_list = []

    for response in my_list:
        joined_list.append(' '.join(response))

    df = pd.DataFrame(joined_list, columns=['n_gram'])
    n_grams = df.n_gram.value_counts().reset_index()
    n_grams.rename(columns={'index': 'n_gram', 'n_gram': 'appearances'}, inplace=True)
    return n_grams

# now we will calculate the sentiment of responses containing each n-gram

df = calc_ngram(esr_q7,2)

responses = convert_response(esr_q7)

resp_df = pd.DataFrame({'responses':responses})

# initialize empty lists
subj_list = []
pol_list = []
df_subj = []
df_pol = []
n_gram_list = []

# we'll only use the first 100 responses, since the relevant ones aren't likely to appear below this cutoff
for i in df.index[:100]:
    filtered_responses = resp_df[resp_df.responses.str.contains(df.n_gram.iloc[i])] # iterate through the index and return the corresponding phrase
    n_gram = df.n_gram.iloc[i]
    n_gram_list.append(n_gram)
# Calculate the sentiment scores and assign to their respective lists
    for response in filtered_responses.responses:
        resp = TextBlob(response)
        subjectivity = resp.sentiment.subjectivity
        polarity = resp.sentiment.polarity
        subj_list.append(subjectivity)
        pol_list.append(polarity)
        subj = np.mean(subj_list)
        pol = np.mean(pol_list)
    df_subj.append(subj)
    df_pol.append(pol)

# compile the lists into a dataframe
list_df = pd.DataFrame({'phrase':n_gram_list,
                        'polarity':df_pol,
                        'subjectivity':df_subj})

def PhraseSentiment(file):

    df = calc_ngram(file,2)


    responses = convert_response(file)

    resp_df = pd.DataFrame({'responses':responses})

    # initialize empty lists
    subj_list = []
    pol_list = []
    df_subj = []
    df_pol = []
    n_gram_list = []

    # we'll only use the first 100 responses, since the relevant ones aren't likely to appear below this cutoff
    for i in df.index[:100]:
        filtered_responses = resp_df[resp_df.responses.str.contains(df.n_gram.iloc[i])] # iterate through the index and return the corresponding phrase
        n_gram = df.n_gram.iloc[i]
        n_gram_list.append(n_gram)
    # Calculate the sentiment scores and assign to their respective lists
        for response in filtered_responses.responses:
            resp = TextBlob(response)
            subjectivity = resp.sentiment.subjectivity
            polarity = resp.sentiment.polarity
            subj_list.append(subjectivity)
            pol_list.append(polarity)
        subj = np.mean(subj_list)
        pol = np.mean(pol_list)
        df_subj.append(subj)
        df_pol.append(pol)

    # compile the lists into a dataframe
    list_df = pd.DataFrame({'phrase':n_gram_list,
                            'polarity':df_pol,
                            'subjectivity':df_subj})
    return list_df

# # run the script on each question and write out the output files
# esr_q7 = 'text_files/esr_q7.txt'
# esrm_q5 = 'text_files/esrm_q5.txt'
# isr_q5 = 'text_files/isr_q5.txt'

# run the script and save the files

# external survey question 7
# n_grams = calc_ngram(esr_q7,2)
# n_grams.to_csv('output_files/n_grams/sent_gram_esr_q7.csv')
#
# # # external survey misclassified question 5
# n_grams = calc_ngram(esrm_q5,2)
# n_grams.to_csv('output_files/n_grams/sent_gram_esrm_q5.csv')
#
# # # # internal survey question 5
# n_grams = calc_ngram(isr_q5,2)
# n_grams.to_csv('output_files/n_grams/sent_gram_isr_q5.csv')
