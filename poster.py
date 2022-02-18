import random
import time
import numpy as np
import plotly.express as px

from images import frec_image, frec_image_plotly, quote_image

class Poster:
    def __init__(self,api, file):
        self.api=api
        self.file=file

    def quote(self, index=0, length_of_quote=200, id=None, inchapter=None, reverse=False):
        if not index:
            #Generates a random index that doesn't have problems if it falls on the last parts
            index=int(random.random()*(len(self.file)-length_of_quote))
        if inchapter:
            word="Capítulo"

            #Gets all the indexes of the character "C"
            capital_letter_indexes=[index for index, value in enumerate(self.file) if value == word[0]]
            chap_indexes=[]

            #Gets all the indexes of the word "Capítulo" and adds it to the chap_indexes list
            for index in capital_letter_indexes:
                for i, _ in enumerate(word):
                    if not self.file[index+i]==word[i]:
                        break
                else:
                    chap_indexes.append(index)
                chap_indexes.append(len(self.file))#to not have problems with last chapter

            #Modules the index to the chapter index, so that the index falls in the chapter
            index=chap_indexes[inchapter+1]+index%(chap_indexes[inchapter+2]-chap_indexes[inchapter+1])
        try:
            dot_indexes=[index for index, value in enumerate(self.file) if value == "."]
            quote_image(self.file, random.choice(dot_indexes), reverse=reverse).save("./images/image.png")
            if id:
                self.api.update_status_with_media("", filename="./images/image.png", in_reply_to_status_id=id)
            else:
                self.api.update_status_with_media("", filename="./images/image.png")
        except Exception as e:
            print(e)

    def frecuency(self,word, id, chars):
        frec_image(self.file, word, chars=chars).save("./images/frecuency.png")
        self.api.update_status_with_media("",filename="./images/frecuency.png", in_reply_to_status_id=id)

    def frecuency_plotly(self, word, id, chars, long):
        frec_image_plotly(self.file, word, long, chars=chars)
        self.api.update_status_with_media("", filename="./images/frecuency.png", in_reply_to_status_id=id)

    def histogram(self, syl, bins=20):
        #Gets all the indexes of the first letter of the word requested
        capital_letter_indexes=[index for index, value in enumerate(self.file) if value == syl[0]]
        word_indexes=[]

        #Gets all the indexes of the word requested and adds it to the word_indexes list
        for index in capital_letter_indexes:
            for i, _ in enumerate(syl):
                if not self.file[index+i]==syl[i]:
                    break
            else:
                word_indexes.append(index)
        try:
            fig = px.histogram(np.array(word_indexes), nbins=bins)
            fig.write_image("./images/plot.png")
        except Exception as e:
            print(e)
        self.api.update_status_with_media("",filename="./images/plot.png", in_reply_to_status_id=id)

    def count(self, word, id):
        #Gets all the indexes of the first letter of the word requested
        capital_letter_indexes=[index for index, value in enumerate(self.file) if value == word[0]]
        word_indexes=[]

        #Gets all the indexes of the word requested and adds it to the word_indexes list
        for index in capital_letter_indexes:
            for i, _ in enumerate(word):
                if not self.file[index+i]==word[i]:
                    break
            else:
                word_indexes.append(index)
        result=len(word_indexes)
        self.api.update_status(f"{word} se repite {result} veces.", in_reply_to_status_id=id)