from ctypes import resize
import spacy
import textwrap as tw
from wand import image
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image
from string import punctuation
import itertools
import random as rng
from google_images_search import GoogleImagesSearch
from . import settings
import os

gis = GoogleImagesSearch(settings.googleApiKey, settings.googleCseId)
nlp = spacy.load('en_core_web_lg')

def get_subject(text):
    doc=nlp(text)
    sub_toks = [str(tok) for tok in doc if (tok.dep_ == "nsubj") and str(tok).lower() not in ["i", "me", "you", "he", "him", "she", "her", "they", "them"]]
    if sub_toks == []:
        return get_hotwords(text)
    return sub_toks 

def get_hotwords(text):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2
    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)
                
    return result # 5

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

colors=itertools.cycle(["#FD0E35", "#5DADEC", "#66FF66", "#FFDB00", "#FF00CC", "#FF007C", "#50BFE6", "#A7F432", "#FFEB00", "#E936A7"])
def createThumbnail(ogtitle, author):
    width, fontsize= 20, 66
    if "?" in ogtitle:
        title=ogtitle.split("?")[0]+"?"
    doc = nlp(ogtitle)
    words = set(get_hotwords(ogtitle))
    print(words)
    title="\n".join(tw.wrap(ogtitle, width=width))
    title.count("\n")
    fontsize=66
    with Image(filename="base.png") as img:
        with Drawing() as ctx:
            substitution=0
            comment_hw = list(set(get_subject(ogtitle)))
            print(comment_hw)
            query=(" ".join(rng.choices(comment_hw, k=(4 if len(comment_hw)>4 else len(comment_hw)))))+rng.choice([" simpsons", " family guy"])
            print(query)
            _search_params = {
                'q': query,
                'num': 1,
                'safe': 'high',
                'fileType': 'png',
            }
            gis.search(search_params=_search_params, path_to_dir='images/', custom_image_name="temp", width=720, height=720)
            imgfile=os.listdir("images")[0]
            topimage=Image(filename="template.png")
            customimg=Image(filename=f'images/{imgfile}')
            ctx.composite(operator="atop", width=720, height=720, top=0, left=600, image=customimg)
            ctx.draw(img)
            img.save(filename='draw-word-wrap1.png')
            ctx.composite(operator="atop", width=1280, height=720, top=0, left=0, image=topimage)
            ctx.draw(img)
            img.save(filename='draw-word-wrap2.png')
            ctx.font_size=fontsize
            print(ctx.get_font_metrics(img, title.split("\n")[0]).text_height*(title.count("\n")+1))
            while not 565<ctx.get_font_metrics(img, title.split("\n")[0]).text_height*(title.count("\n")+1)<685:
                old_fontsize=fontsize
                fontsize+=6
                width=round((width*old_fontsize)/fontsize, 0)
                print(width)
                title="\n".join(tw.wrap(ogtitle, width=width))
                ctx.font_size=fontsize
                print(ctx.get_font_metrics(img, title.split("\n")[0]).text_height*(title.count("\n")+1))
            y=136+fontsize
            substitution=-int(ctx.get_font_metrics(img, title.split("\n")[0]).text_height-685/(title.count("\n")+1))
            if substitution<0:
                substitution=0
            print(fontsize)
            print(width)
            #y+=-int(((ctx.get_font_metrics(img, title.split("\n")[0]).text_height*(title.count("\n")+1))-635)/2)
            ctx.font = "fonts/titleFont.ttf"
            for line in title.split("\n"):
                white={}
                colored={}
                i=0
                for word in line.split(" "):
                    if word in words:
                        colored.update({i: word})
                    else:
                        white.update({i: word})
                    i+=1
                x=30
                i=0
                for i in range(len(line.split(" "))):
                    if i in colored:
                        ctx.fill_color = Color(next(colors))
                        currentword=colored[i]+" "
                    else:
                        ctx.fill_color = Color("WHITE")
                        currentword=white[i]+" "
                    ctx.text(x, y, currentword)
                    ctx.draw(img)
                    metric=int(ctx.get_font_metrics(img, currentword).text_width)
                    x+=metric
                y+=int(ctx.get_font_metrics(img, line).character_height*0.91)+substitution
            ctx.font="fonts/authorFont.ttf"
            ctx.font_size=45
            ctx.fill_color=Color("#0645ad")
            ctx.text(388, 129, author)
            ctx.draw(img)

        img.save(filename='thumbnail.png')
        os.remove(f"images/{imgfile}")
        
#createThumbnail("Steve Irwin has you pinned down in a headlock, what cool facts does he tell the audience about you and your habitat?", "u/zombiepiemaster")

#=> FontMetrics(character_width=25.0,
#               character_height=25.0,
#               ascender=23.0,
#               descender=-5.0,
#               text_width=170.0,
#               text_height=29.0,
#               maximum_horizontal_advance=50.0,
#               x1=0.0,
#               y1=0.0,
#               x2=19.21875,
#               y2=18.0,
#               x=170.0,
#               y=0.0)
# >520 <545
"""
import pyttsx as tts

engine = tts.init(driverName="espeak")
voices = engine.getProperty("voices")
for voice in voices:
        print(voice.id, voice.name)
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 165)
engine.save_to_file("Have you ever been drunk or high and came up with this truly amazing idea but then became sober and realized it wasn't as amazing as you thought it was? If so, what was the idea?")
engine.runAndWait()
"""