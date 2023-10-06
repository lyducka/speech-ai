import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()
tiktok_token = os.environ.get('TIKTOK_TOKEN')

import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def prompt_openai(doc):
    import openai
    openai.api_type = "azure"
    openai.api_base = os.getenv('OPENAI_BASE')
    openai.api_version = "2022-12-01"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
    Create a summary of the text below.

    '{doc}'
    """

    response = openai.Completion.create(
        engine=os.getenv('OPENAI_DEPLOYMENT'),
        prompt=prompt,
        temperature=0.5,
        max_tokens=1096,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    return response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

def estimate_token_count(text):
    encoding = tiktoken.get_encoding('gpt2')
    num_tokens = len(encoding.encode(text))
    return num_tokens

def split_document(text, out_documents):
    tc = estimate_token_count(text)
    if tc > 2500:
        sentences = list(sent_tokenize(text))
        midpoint = int(len(sentences)/2)
        chunk_1 = ' '.join(sentences[0:midpoint])
        chunk_2 = ' '.join(sentences[midpoint:])
        split_document(chunk_1, out_documents)
        split_document(chunk_2, out_documents)
    else:
        out_documents.append(text)

def summarize_all_documents(documents):
    summarized_docs = []
    for index, doc in enumerate(documents):
        print(str(index) + '/' + str(len(documents)))
        split_documents = []
        split_document(doc, split_documents)
        for sdoc in split_documents:
            summarized_docs.append(str(prompt_openai(sdoc)))
    return summarized_docs

def create_single_summary(documents):
    summaries = summarize_all_documents(documents)
    if len(summaries)==1:
        return summaries[0]
    else:
        return create_single_summary([' '.join(summaries)])
    
documents = []

# https://www.gutenberg.org/files/164/164-h/164-h.htm
# resp = requests.get('https://notes.966885.xyz/posts/English-text-test/')
# soup = BeautifulSoup(resp.text, 'html.parser')
# # chapters = soup.find_all('div', class_='chapter')
# chapters = soup.find_all('div', class_='post-content')
# for c in chapters:
#     if len(c.text)>100:
#         documents.append(c.text)

# get local file instead
with open('data/Chinese-text-test.txt', 'r') as f:
    documents.append(f.read())

summary = create_single_summary(documents)
print(summary)    