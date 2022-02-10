from dotenv import load_dotenv
import tweepy
import os
from Poster import Poster


class Twitter:
    def __init__(self, file):
        load_dotenv()
        auth = tweepy.OAuthHandler(os.getenv("APIKEY"), os.getenv("APIKEY_SECRET"))
        auth.set_access_token(os.getenv("ATOKEN"),os.getenv("ATOKEN_SECRET"))

        self.api=tweepy.API(auth, wait_on_rate_limit=True)
        self.Poster = Poster(self.api, file)

    def answermention(self, id, command):
        try:
            if command[0]=="cita":
                if command[2]=="reverso":
                    self.Poster.quote(index=int(command[1][8:]), id=id, reverse=True)
                elif command[2][:8]=="capítulo=":
                    self.Poster.quote(index=int(command[1][8:]), id=id, inchapter=int(command[2][8:]))
                else:
                    self.Poster.quote(index=int(command[1][8:]), id=id)
            elif command[0]=="contar":
                self.Poster.count(command[1][8:], id)
            elif command[0]=="histograma":
                self.Poster.histogram(command[1][8:])      
            elif command[0]=="frecuencia":
                if command[3]=="plotly":
                    self.Poster.frecuency_plotly(command[1][8:], id, int(command[2]), int(command[4]))
                else:
                    self.Poster.frecuency(command[1][8:], id, int(command[2]))
            else:
                self.api.update_status(f"Formato incorrecto.\nUsa los comandos en el comentario fijado de mi perfil.", in_reply_to_status_id=id)
        except:
            self.api.update_status(f"Se produjo un error. Revisa si el formato está escrito correctamente.", in_reply_to_status_id=id)
        with open("./textfiles/lastid.txt", "w", encoding="utf-8") as fi:
                    fi.write(str(id))
    
    def getmentions(self):
        lowest_id=int(open("lastid.txt", "r").read())
        mentions=self.api.mentions_timeline(since_id=lowest_id+1)
        return {mention.id:mention.text[15:].strip().split() for mention in mentions}