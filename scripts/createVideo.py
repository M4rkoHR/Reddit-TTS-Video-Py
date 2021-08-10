import moviepy.editor as mp
from prawcore.auth import ScriptAuthorizer
from . import settings
import textwrap as tw
import praw
import ffmpeg
import random as rng
import os


def save_to_file(text, filename):
    with open('temp.txt', 'w') as f:
        f.write(text)
    os.system(f"balcon.exe -f temp.txt -n \"ScanSoft Daniel_Full_22kHz\" -w {filename}")

def createVideo(v_length=603, sub="askreddit", top="month"):
    reddit = praw.Reddit(client_id=settings.prawClientID,
                        client_secret=settings.prawClientSecret,
                        user_agent=settings.prawUserAgent)
    subreddit = reddit.subreddit(sub)
    titlefont="IBM Plex Sans-Medium"
    authorfont="IBM Plex Sans-Regular"
    subredditFont="IBM Plex Sans-Bold"
    commentFont="Noto Sans-Regular"
    bgColor=(26, 26, 27)
    screensize=(1920, 1080)
    clips=[]
    index=rng.randint(0, 100)
    skipped=0
    realtitle=None
    for submission in subreddit.top(top):
        if skipped<index:
            skipped+=1
            continue
        title="\n".join(tw.wrap(submission.title, width=screensize[0]/30))
        try:
            op="u/"+submission.author.name
        except:
            op="[deleted]"
        #submission.comment_sort = "top"
        comments=submission.comments.list()
        score=str(round(submission.score/1000, 1))+"k"
        print(title)
        save_to_file(submission.title, 'temp\\title.wav')
        realtitle=submission.title
        duration=round(float(ffmpeg.probe('temp\\title.wav')['format']['duration']), 2)+1
        length=duration
        print(length)
        OPClip = mp.TextClip(op, color='turquoise', font=authorfont, fontsize=40, align="west").set_position((10, 10))
        txtClip = mp.TextClip(title,color='white', font=titlefont, fontsize=48, align="west").set_position("center").set_duration(duration).on_color(color=bgColor, size=screensize)
        upvotes = mp.TextClip(score,color='white', font=titlefont, fontsize=24, align="west").set_position((30, 540-24))
        uvdv= mp.ImageClip("assets/upvotedownvote.jpg").resize((76, 172)).set_position((15, 540-94))
        titleclip = mp.CompositeVideoClip([txtClip, OPClip, uvdv, upvotes]).set_duration(duration).set_audio(mp.AudioFileClip("temp/title.wav"))
        clips.append(titleclip)
        print(title)
        i=0
        while int(length)<v_length:
            comment_text="\n".join(tw.wrap(comments[i].body, width=85))
            cscore=str(round(comments[i].score/1000, 1))+"k"
            try:
                author="u/"+comments[i].author.name
            except:
                author="[deleted]"
            save_to_file(comments[i].body, f'temp/temp{i}.wav')
            duration=round(float(ffmpeg.probe(f'temp/temp{i}.wav')['format']['duration']), 2)+1
            length+=duration
            txtClip = mp.TextClip(comment_text,color='white', font=commentFont, fontsize=40, align="west").set_position("center").set_duration(duration).on_color(color=bgColor, size=screensize)
            authorClip = mp.TextClip(author, color='turquoise', font=commentFont, fontsize=40, align="west").set_position((10, 10))
            cupvotes = mp.TextClip(cscore,color='white', font=titlefont, fontsize=24, align="center").set_position((30, 540-24))
            cuvdv= mp.ImageClip("assets/upvotedownvote.jpg").resize((76, 172)).set_position((15, 540-94))
            finalclip = mp.CompositeVideoClip([txtClip, authorClip, cuvdv, cupvotes]).set_duration(duration).set_audio(mp.AudioFileClip(f"temp/temp{i}.wav"))
            print(comment_text, author)
            clips.append(finalclip)
            i+=1
            print(length)
        break
    print("rendering")
    video = mp.concatenate_videoclips(clips)
    video.write_videofile(f"export/video.mp4", fps=24, threads=4)
    return realtitle, op