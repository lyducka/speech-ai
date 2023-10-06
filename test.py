import requests
from bs4 import BeautifulSoup

documents = []

# https://www.gutenberg.org/files/164/164-h/164-h.htm
resp = requests.get('https://notes.966885.xyz/posts/English-text-test/')
soup = BeautifulSoup(resp.text, 'html.parser')
chapters = soup.find_all('div', class_='post-content')
for c in chapters:
    if len(c.text)>100:
        documents.append(c.text)

print(documents)