from PIL import Image, ImageDraw
import pandas as pd
import re
import plotly.express as px

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

def frec_image_plotly(file, word, nsyllabes,chars=2):

    frecuencies = frecafter(file, word, nchars=chars)
    frecuencies_trans = {"SÍLABAS":[f"'{key}'" for key, _ in frecuencies.items()],
                         "FRECUENCIA":[value for _, value in frecuencies.items()]}
    frecdf = pd.DataFrame(frecuencies_trans)
    frecdf = frecdf.iloc[:nsyllabes]
    fig  = px.bar(data_frame=frecdf, x="SÍLABAS", y="FRECUENCIA")
    fig.write_image("frecuency.png")