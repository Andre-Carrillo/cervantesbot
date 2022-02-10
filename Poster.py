import random
import time
import numpy as np

from frec_image import *
from quoteimage import quoteimage

class Poster:
    def __init__(self,api, file):
        self.api=api
        self.file=file

    def quote(self, index=0, length_of_quote=200, id=None, inchapter=None, reverse=False):
        if not index:
            index=int(random.random()*(len(self.file)-length_of_quote))
        if inchapter:
            word="Capítulo"
            capital_letter_indexes=[index for index, value in enumerate(self.file) if value == word[0]]
            chap_indexes=[]
            for index in capital_letter_indexes:
                for i, _ in enumerate(word):
                    if not self.file[index+i]==word[i]:
                        break
                else:
                    chap_indexes.append(index)
                chap_indexes.append(len(self.file))#to not have problems with last chapter
            index=chap_indexes[inchapter+1]+index%(chap_indexes[inchapter+2]-chap_indexes[inchapter+1])
        try:
            # api.update_status_(quote, in_reply_to_status_id=id)
            dot_indexes=[index for index, value in enumerate(self.file) if value == "."]
            quoteimage(self.file, random.choice(dot_indexes), reverse=reverse).save("image.png")
            if id:
                self.api.update_status_with_media("",filename="image.png", in_reply_to_status_id=id)
            else:
                self.api.update_status_with_media("", filename="image.png")
        except Exception as e:
            print(f"[{time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}-{time.localtime()[1:3]}]"+f"Could not tweet: {e}"+"\n")

    def frecuency(self,word, id, chars):
        frec_image(self.file, word, chars=chars).save("frecuency.png")
        self.api.update_status_with_media("",filename="frecuency.png", in_reply_to_status_id=id)

    def frecuency_plotly(self, word, id, chars, long):
        frec_image_plotly(self.file, word, long, chars=chars)
        self.api.update_status_with_media("", filename="frecuency.png", in_reply_to_status_id=id)

    def histogram(self, syl, bins=20):
        capital_letter_indexes=[index for index, value in enumerate(self.file) if value == syl[0]]
        word_indexes=[]
        for index in capital_letter_indexes:
            for i, _ in enumerate(syl):
                if not self.file[index+i]==syl[i]:
                    break
            else:
                word_indexes.append(index)
        try:
            fig = px.histogram(np.array(word_indexes), nbins=bins)
            fig.write_image("./plot.png")
        except Exception as e:
            print(e)
        self.api.update_status_with_media("",filename="plot.png", in_reply_to_status_id=id)

    def count(self, word, id):
        capital_letter_indexes=[index for index, value in enumerate(self.file) if value == word[0]]
        word_indexes=[]
        for index in capital_letter_indexes:
            for i, _ in enumerate(word):
                if not self.file[index+i]==word[i]:
                    break
            else:
                word_indexes.append(index)
        result=len(word_indexes)
        self.api.update_status(f"{word} se repite {result} veces.", in_reply_to_status_id=id)