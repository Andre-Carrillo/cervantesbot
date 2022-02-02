import tweepy
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("APIKEY"), os.getenv("APIKEY_SECRET"))
auth.set_access_token(os.getenv("ATOKEN"),os.getenv("ATOKEN_SECRET"))

api=tweepy.API(auth)

bookpath="./libro.txt"
file = open(bookpath, "r", encoding="utf-8").read()

def tweet_quote(index=0, len_of_quote=200, id=None):
    # f = open(bookpath, "r", encoding="utf-8").read()
    if not index:
        index=int(random.random()*(len(f)-len_of_quote))
    quote=file[index:index+len_of_quote]
    try:
        api.update_status(quote, in_reply_to_status_id=id)
    except:
        print("Could not tweet")

def countword(word):
    # f = open(bookpath, "r", encoding="utf-8").read()
    capital_letter_indexes=[index for index, value in enumerate(file) if value == word[0]]
    word_indexes=[]
    for index in capital_letter_indexes:
        for i, lettre in enumerate(word):
            if not file[index+i]==word[i]:
                break
        else:
            word_indexes.append(index)
    return(len(word_indexes))


def mainloop():
    i=0
    lowest_id=int(open("lastid.txt", "r").read())+1
    print("Starting main loop...")
    while True:
        mentions=api.mentions_timeline(since_id=lowest_id)
        print(f"Extracted {len(mentions)} mentions")
        if mentions:
            for mention in mentions:
                raw_command=mention.text[15:]
                command=raw_command.strip().split(" ")
                if command[0]=="cita":
                    tweet_quote(index=int(command[1][8:]), id=mention.id)
                elif command[0]=="contar":
                    api.update_status(f"{command[1][8:]} se repite {countword(command[1][8:])} veces", in_reply_to_status_id=mention.id)
                with open("lastid.txt", "w", encoding="utf-8") as fi:
                    fi.write(mention.id)
                print(f"Command: '{command}' answered.")

        if i%2160==0:
            dot_indexes=[index for index, value in enumerate(file) if value == "."]
            tweet_quote(index=random.choice(dot_indexes))
            print("Quote tweeted.")
        i+=1
        time.sleep(10)
mainloop()