from bs4 import BeautifulSoup
import sys
import re
import pickle
import csv
from datetime import datetime
from collections import defaultdict
import pandas as pd

def save_obj(obj):
    # sys.setrecursionlimit(3000000)
    for key in obj:
        name = re.sub(r"[ ,]+","_",key)
        obj[key] = obj[key].sort_values(['timestamp'])
        obj[key].to_csv('msg/'+name+'.csv',index=False)


def parse_messages(soup,messages_dict):
    divOfThreads = list(soup.select('.contents > div'))


    """for each group of divs containing <div class="thread">"""
    for div in range(0, len(divOfThreads)):

        """for each thread of messages inside each div"""
        threads = divOfThreads[div].select('.thread')
        for threadDiv in range (0, len(threads)):

            """select all the messages inside each thread"""
            p = list(threads[threadDiv])
            users = p[0]
            if len(users) < 100:
                if users not in messages_dict:
                    messages_dict[users] =  pd.DataFrame(columns=['user','timestamp','message'])

                    for x in range(1,len(p),2):
                        user = p[x].select('.user')[0].text
                        meta = p[x].select('.meta')[0].text
                        meta = meta[:meta.find("UTC")-1]
                        date_object = datetime.strptime(meta, '%A, %B %d, %Y at %I:%M%p')
                        meta = "{:%Y-%m-%d %H:%M}".format(date_object)
                        text = p[x+1].text
                        messages_dict[users] =  messages_dict[users].append(pd.DataFrame([[user,meta,text]],columns=['user','timestamp','message']), ignore_index=True)

    return messages_dict

if __name__ == "__main__":

    soup = BeautifulSoup(open("messages_en.htm"), "html.parser")


    msg_dict = dict()
    msg_dict = parse_messages(soup,msg_dict)
    save_obj(msg_dict)
