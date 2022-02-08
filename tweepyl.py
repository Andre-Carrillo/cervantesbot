import tweepy
import random
import time
import os
from dotenv import load_dotenv
# import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

from test import quoteimage
from frec_image import frec_image, frec_image_plotly

#TODOS
#Wrong request answer //done
#histograma de frecuencia de una sílaba//done
#quotes al revés//done
#hacerlo con plotly//done
#Most common 2-letter-syllabe that are after a certain word//done
#creo que el quoter por capítulo funciona mal xd
#hacer que la imagen de frecuencias también pueda ser por plotly//done


def tweet_frec(word, id, chars):
    frec_image(file, word, chars=chars).save("frecuency.png")
    api.update_status_with_media("",filename="frecuency.png", in_reply_to_status_id=id)

def tweet_frec_plotly(word, id, chars, long):
    frec_image_plotly(file, word, long, chars=chars)
    api.update_status_with_media("", filename="frecuency.png", in_reply_to_status_id=id)

def tweet_quote(index=0, len_of_quote=200, id=None, reverse=False, inchapter=None):
    if not index:
        index=int(random.random()*(len(file)-len_of_quote))
    if inchapter:
        word="Capítulo"
        capital_letter_indexes=[index for index, value in enumerate(file) if value == word[0]]
        chap_indexes=[]
        for index in capital_letter_indexes:
            for i, _ in enumerate(word):
                if not file[index+i]==word[i]:
                    break
            else:
                chap_indexes.append(index)
            chap_indexes.append(len(file))#to not have problems with last chapter
        index=chap_indexes[inchapter+1]+index%(chap_indexes[inchapter+2]-chap_indexes[inchapter+1])
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
    try:
        fig = px.histogram(np.array(word_indexes), nbins=bins)
        fig.write_image("./plot.png")
    except Exception as e:
        print(e)

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
    tweetpendiente=False
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
                        elif command[2][:8]=="capítulo=":
                            tweet_quote(index=int(command[1][8:]), id=mention.id, inchapter=int(command[2][8:]))
                        else:
                            tweet_quote(index=int(command[1][8:]), id=mention.id)
                    elif command[0]=="contar":
                        api.update_status(f"{command[1][8:]} se repite {countword(command[1][8:])} veces.", in_reply_to_status_id=mention.id)
                    elif command[0]=="histograma":
                        sylhist(command[1][8:])
                        api.update_status_with_media("",filename="plot.png", in_reply_to_status_id=mention.id)                    
                    elif command[0]=="frecuencia":
                        if command[3]=="plotly":
                            tweet_frec_plotly(command[1][8:], mention.id, int(command[2]), int(command[4]))
                        else:
                            tweet_frec(command[1][8:], mention.id, chars=int(command[2]))

                    else:
                        api.update_status(f"Formato incorrecto.\nUsa los comandos 'cita' o 'contar' seguidos de 'empieza' o 'palabra' seguido de tu pedido.", in_reply_to_status_id=mention.id)
                except:
                    api.update_status(f"Se produjo un error. Revisa si el formato está escrito correctamente.", in_reply_to_status_id=mention.id)


                log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+f"Command: '{command}' answered. Mention{mention.id}"+"\n")
                with open("lastid.txt", "w", encoding="utf-8") as fi:
                    fi.write(str(mention.id))
                    log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+f"Changed lastid to {mention.id}"+"\n")
                fi.close()
        #if (i+1)%(360*hours)==0:
        if (i+1)%1440==0:
            try:
                tweet_quote(index=random.choice(dot_indexes)+1)
                log.write(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+"Quote tweeted."+"\n")
                tweetpendiente=False
            except:
                tweetpendiente=True
        if not tweetpendiente:
            i+=1
        log.close()
        time.sleep(10)

if __name__=="__main__":
    log = open("./log.txt", "a")
    load_dotenv()

    auth = tweepy.OAuthHandler(os.getenv("APIKEY"), os.getenv("APIKEY_SECRET"))
    auth.set_access_token(os.getenv("ATOKEN"),os.getenv("ATOKEN_SECRET"))

    api=tweepy.API(auth, wait_on_rate_limit=True)

    bookpath="./libro.txt"
    file = open(bookpath, "r", encoding="utf-8").read()
    while True:
        try:
            mainloop(4)
        except Exception as e:
            log.writelines(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+"Process ended due to an error"+"\n")
            log.writelines(str(e)+"\n")


