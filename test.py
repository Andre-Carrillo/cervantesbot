from PIL import Image, ImageDraw
import textwrap

def quoteimage(book, rn=0, reverse=False): 
    dot_indexes=[index for index, value in enumerate(book) if value == "."]
    index , end= dot_indexes[rn-1:rn+1]
    quote=book[index+1: end+1]
    if reverse:
        quote = quote[::-1]
    quote = textwrap.fill(quote, 40)
    nlines=quote.count("\n")
    print(nlines)

    out = Image.new("RGB", (270, nlines*15-5), (255, 255, 255))
    d = ImageDraw.Draw(out)
    d.multiline_text((10, 10), quote, fill=(0, 0, 0))

    # out.save("image.png")
    return out
