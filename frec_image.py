from PIL import Image, ImageDraw
import pandas as pd
import re
def frecafter(file, word, nchars=2):
    capital_letter_indexes=[index for index, value in enumerate(file) if value == word[0]]
    chap_indexes=[]
    for index in capital_letter_indexes:
        for i, _ in enumerate(word):
            if not file[index+i]==word[i]:
                break
        else:
            chap_indexes.append(index)
    syllabes=[]
    for index in chap_indexes:
        syllabes.append(file[index+len(word):index+len(word)+nchars:])
    syllabes[0]
    df = pd.Series(syllabes)
    return dict(df.value_counts())

def frec_image(file, word, chars=2):

    text = str(frecafter(file, word, nchars=chars))
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"\b,\s", "\n",text)
    text = "syllabe: frecuency \n"+text

    out = Image.new("RGB", (200, 260), (255, 255, 255))
    d = ImageDraw.Draw(out)
    d.multiline_text((10, 10), text, fill=(0, 0, 0))

    # out.save("image.png")
    return out
