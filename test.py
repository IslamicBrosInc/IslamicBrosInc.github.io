import requests
from bs4 import BeautifulSoup

search = input('your search terms here.')
url = 'https://www.google.com/search'

headers = {
	'Accept' : '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}
parameters = {'q': search}

content = requests.get(url, headers = headers, params = parameters).text
soup = BeautifulSoup(content, 'html.parser')

search = soup.find(id = 'search')
link = search.find('a')

URL = link['href']
print(URL)

page = requests.get(URL)


soup1 = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")
p = blog_titles = soup1.findAll(['p'])
for title in blog_titles:
    print(title.text)
