import tweepy
import random
import time
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

from test import quoteimage

## TODOS
#Wrong request answer //done
#histograma de frecuencia de una sílaba//done
#quotes al revés//done
#hacerlo con plotly
#si hago videos, que lo narre con voz de loquendo

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("APIKEY"), os.getenv("APIKEY_SECRET"))
auth.set_access_token(os.getenv("ATOKEN"),os.getenv("ATOKEN_SECRET"))

api=tweepy.API(auth, wait_on_rate_limit=True)

bookpath="./libro.txt"
file = open(bookpath, "r", encoding="utf-8").read()

def tweet_quote(index=0, len_of_quote=200, id=None, reverse=False):
    if not index:
        index=int(random.random()*(len(file)-len_of_quote))
    quote=file[index:index+len_of_quote]
    try:
        # api.update_status_(quote, in_reply_to_status_id=id)
        quoteimage(file, index, reverse=reverse).save("image.png")
        api.update_status_with_media("",filename="image.png", in_reply_to_status_id=id)
    except Exception as e:
        print(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+f"Could not tweet: {e}"+"\n")

def sylhist(syl, bins=20):
    capital_letter_indexes=[index for index, value in enumerate(file) if value == syl[0]]
    word_indexes=[]
    for index in capital_letter_indexes:
        for i, _ in enumerate(syl):
            if not file[index+i]==syl[i]:
                break
        else:
            word_indexes.append(index)
    plt.hist(word_indexes, bins=bins)
    plt.savefig("./plot.png")

def countword(word):
    capital_letter_indexes=[index for index, value in enumerate(file) if value == word[0]]
    word_indexes=[]
    for index in capital_letter_indexes:
        for i, _ in enumerate(word):
            if not file[index+i]==word[i]:
                break
        else:
            word_indexes.append(index)
    return(len(word_indexes))


def mainloop(hours):
    i=0
    log = open("./log.txt", "a")
    log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+"Starting main loop..."+"\n")
    dot_indexes=[index for index, value in enumerate(file) if value == "."]
    while True:
        log = open("./log.txt", "a")
        lowest_id=int(open("lastid.txt", "r").read())
        mentions=api.mentions_timeline(since_id=lowest_id+1)
        log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+f"Extracted {len(mentions)} mentions"+"\n")
        if mentions:
            for mention in mentions:
                raw_command=mention.text[15:]
                command=raw_command.strip().split(" ")
                try:
                    if command[0]=="cita":
                        if command[2]=="reverso":
                            tweet_quote(index=int(command[1][8:]), id=mention.id, reverse=True)
                        else:
                            tweet_quote(index=int(command[1][8:]), id=mention.id)
                    elif command[0]=="contar":
                        api.update_status(f"{command[1][8:]} se repite {countword(command[1][8:])} veces.", in_reply_to_status_id=mention.id)
                    elif command[0]=="histograma":
                        sylhist(command[1][8:])
                        api.update_status_with_media("",filename="plot.png", in_reply_to_status_id=mention.id)                    
                    else:
                        api.update_status(f"Formato incorrecto.\nUsa los comandos 'cita' o 'contar' seguidos de 'empieza' o 'palabra' seguido de tu pedido.", in_reply_to_status_id=mention.id)
                except:
                    api.update_status(f"Se produjo un error. Revisa si el formato está escrito correctamente.", in_reply_to_status_id=mention.id)


                log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+f"Command: '{command}' answered. Mention{mention.id}"+"\n")
                with open("lastid.txt", "w", encoding="utf-8") as fi:
                    fi.write(str(mention.id))
                    log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+f"Changed lastid to {mention.id}"+"\n")
                fi.close()
        if (i+1)%(360*hours)==0:
            tweet_quote(index=random.choice(dot_indexes)+1)
            
            log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+"Quote tweeted."+"\n")
        i+=1
        log.close()
        time.sleep(10)
log = open("./log.txt", "a")
try:
    mainloop(4)
except Exception as e:
    log.writelines(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+"Process ended due to an error"+"\n")
    log.writelines(str(e)+"\n")


