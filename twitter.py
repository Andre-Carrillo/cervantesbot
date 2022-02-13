from dotenv import load_dotenv
import tweepy
import os
from poster import Poster


class Twitter:
    def __init__(self, file):
        load_dotenv()
        auth = tweepy.OAuthHandler(os.getenv("APIKEY"), os.getenv("APIKEY_SECRET"))
        auth.set_access_token(os.getenv("ATOKEN"),os.getenv("ATOKEN_SECRET"))

        self.api=tweepy.API(auth, wait_on_rate_limit=True)
        self.Poster = Poster(self.api, file)

    def answermention(self, id, command):
        try:
            match command[0]:
                case "cita":
                    if command[2]=="reverso":
                        self.Poster.quote(index=int(command[1][8:]), id=id, reverse=True)
                    elif command[2][:8]=="capítulo=":
                        self.Poster.quote(index=int(command[1][8:]), id=id, inchapter=int(command[2][8:]))
                    else:
                        self.Poster.quote(index=int(command[1][8:]), id=id)
                case "contar":
                    self.Poster.count(command[1][8:], id)
                case "histograma":
                    self.Poster.histogram(command[1][8:])      
                case "frecuencia":
                    if command[3]=="plotly":
                        self.Poster.frecuency_plotly(command[1][8:], id, int(command[2]), int(command[4]))
                    else:
                        self.Poster.frecuency(command[1][8:], id, int(command[2]))
                case _:
                    self.api.update_status(f"""Formato incorrecto.\nUsa los comandos
                                            en el comentario fijado de mi perfil.""", in_reply_to_status_id=id)
        except Exception as e:
            self.api.update_status(f"""Se produjo un error. Revisa si el formato
                                    está escrito correctamente.""", in_reply_to_status_id=id)
            print(e)
        with open("./textfiles/lastid.txt", "w", encoding="utf-8") as fi:
                    fi.write(str(id))
    
    def getmentions(self):
        lowest_id=int(open("./textfiles/lastid.txt", "r").read())
        mentions=self.api.mentions_timeline(since_id=lowest_id+1)

        #Returns a dictionary that has the id of every mention and also has a list of the commands
        #{id:command_list}
        return {mention.id:mention.text[15:].strip().split() for mention in mentions}