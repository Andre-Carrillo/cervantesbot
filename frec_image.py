from PIL import Image, ImageDraw
from tweepyl import frecafter
import re

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
