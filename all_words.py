import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from stop_words import get_stop_words

name = sys.argv[1]
messages = pd.read_csv("msg/"+name+".csv").fillna(" ")

to_be_removed = ".,!?"

stop_words = get_stop_words('german')

count_dict = dict()
for index,row in messages.iterrows():
    if row['user'] not in count_dict:
        count_dict[row['user']] = dict()

    row['message'] = row['message'].lower()
    for c in to_be_removed:
        row['message'] = row['message'].replace(c, '')

    list_of_words = row['message'].split()
    for word in list_of_words:
        if word not in count_dict[row['user']]:
            count_dict[row['user']][word] = 0
        count_dict[row['user']][word] += 1

print("finished")
noWords = 51
for user in count_dict:
    ord_dict = OrderedDict(sorted(count_dict[user].items(), key=lambda t: t[1], reverse=True))
    values = []
    keys = ["important","yes","meet","uni","learn","study",":)","watch","already","edu","strange","love","meeting","startup","college","course","pizza","perhaps","relationship","explain","develope","town","stackoverflow","everyone","idea","energy","friend","performance","happy","afternoon","green","theory","trip","time","news","travel","freedom","nobody","alone","sorry","thx","return","comm","man","understand","woman","pretty","nervous","downside","australia"]
    counterUniqueWords = len(ord_dict.items())
    counterAllWords = 0
    counter = 0
    for i, (key, value) in enumerate(ord_dict.items()):
        counterAllWords += value
        if key in stop_words:
            continue
        counter += 1
        if counter >= noWords:
            continue
        # keys.append(key)
        values.append(value)

    plt.xkcd()
    fig = plt.figure()
    plt.title('User: '+user+' words: '+str(counterAllWords)+', different: '+str(counterUniqueWords))
    plt.bar(range(len(keys)), values, align='center')
    plt.xticks(range(len(keys)), keys)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.xlim(-1, noWords)
    fig.tight_layout()
    fig.savefig('img/all_words_'+name+'_'+user+'.jpg')
