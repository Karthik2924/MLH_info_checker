import pathlib
import textwrap
import gradio as gr


import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown

#pip install google-search python
from googlesearch import search

import bs4 as bs
import urllib.request

## Import the key safely
GOOGLE_API_KEY = "Enter API key here"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


import gradio as gr
from transformers import pipeline
import numpy as np

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-medium.en")

def transcribe(audio):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    return transcriber({"sampling_rate": sr, "raw": y})["text"]

def llm_output(txt,query):
    prompt= " The above is an information source, does the main idea of the source verify the following query. answer in around 20 words "
    # prompt2 = "List the claims in the following text "
    response = model.generate_content(txt + prompt + query)
    return response.candidates[0].content.parts[0].text

def process(text,num_searchs=3):
  url_list = get_urls( text,num_searchs)
  processed = []
  unp = []
  for i in  url_list:
      try:
          processed.append(process_url(i))
      except:
          unp.append(i)
  llm_outs = []
  for i in processed:
    llm_outs.append(llm_output(i,text))#+'\n')
  return llm_outs,url_list

def main(text, num_searchs,audio,video):
    if text != "":
      ans,sources = process(text,num_searchs)
    elif audio!= None:
      txt = transcribe(audio)
      ans,sources = process(text,num_searchs)
    elif video!=None:
      txt = transcribe(video)
      ans,sources = process(text,num_searchs)
    else:
      ans = "please submit an input"
      return ans
    
    final_ans = ""
    for i in ans:
      final_ans+=i
      final_ans+='\n'
    final_ans+= "The following are the sources" + '\n'
    for i in sources:
      final_ans+=i
      final_ans+='\n'

    return final_ans



demo = gr.Interface(
    fn=main,
    inputs=["text", gr.Slider(value=2, minimum=1, maximum=10, step=1),"audio","video"],
    outputs=[gr.Textbox(label="output", lines=10)],
)

if __name__ == "__main__":
    demo.launch(debug = True)
