from pytube import YouTube
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import re
import json as json
import whisper
import pandas as pd
import os
import openai

openai.api_key = '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'


class FatwaCard:
  def __init__(self,url):
      self.url = url
      self.title = None
      self.filename=None
      self.transcript_text = None
      self.video_summary = None
    
  def set_title_and_filename(self):
      session = HTMLSession()
      resp = session.get(self.url)
      soup = bs(resp.html.html, "html.parser")
      title = soup.find("meta", itemprop="name")['content']
      self.title = title
      self.filename = f'{self.title}.mp4'

  def set_transcript(self):
      audio_file = YouTube(self.url).streams.filter(only_audio=True).first().download(filename=self.filename)
      model = whisper.load_model("tiny")
      result = model.transcribe(self.filename, language="en", fp16=False, verbose=True)
      transcript_text = result["text"]
      self.transcript_text = transcript_text

    
  def set_summary(self):
      completion = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "user", "content": f"create a summarization of this text, do it without commenting on the text. write the text as if the summarized version is the text itself: {self.transcript_text}. FYI: the title of this video is {self.filename}. Please do not make up your own words, only restating from the article."}
          ]
      )

      video_summary = completion.choices[0].message.content
      self.video_summary = video_summary
      # with open(f'{title}.txt', 'w') as f:
      #     f.write(transcript_text)

      return video_summary
  
  def remove_video_from_server(self):
      os.remove(self.filename)

  def get_title_and_filename(self):
      return self.title,self.filename
  def get_transcript(self):
      return self.transcript_text
  def get_summary(self):
      return self.video_summary