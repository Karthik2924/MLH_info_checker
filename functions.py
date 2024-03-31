import pathlib
import textwrap

import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown

#pip install google-search python
from googlesearch import search

import bs4 as bs
import urllib.request


## Import the key safely
GOOGLE_API_KEY = 'AIzaSyBYv4rXJa5ft99khetg4PNEnYGE2qOd3pg'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def get_urls(query,num_results):
    return list(search(term = query,num_results=num_results))

def process_url(url):
    source = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(source,'lxml')
    txt = soup.text.replace('\n','').replace('\t','')
    return txt


def llm_output(txt,type):
    prompt1 = "Give a one line explanation of the main idea of the following content"
    prompt2 = "List the claims "
    response = model.generate_content()
