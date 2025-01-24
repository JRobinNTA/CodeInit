import json
import requests
from bs4 import BeautifulSoup

with open('./cookies.json') as f:
	cookies = json.load(f)

length = len(cookies)

cookie_passer = dict()
for i in range(length):
    cookie_passer[cookies[i]['Name raw']] = cookies[i]['Content raw']


url = "https://sites.google.com/nitc.ac.in/interviewdiaries/oracle?authuser=1"
response = requests.get(url, cookies=cookie_passer)
soup = BeautifulSoup(response.content, "html.parser")
text = soup.find_all('p')
links = soup.find_all('a', href=True)

text_content = "\n".join([element.get_text() for element in text])


# text_bulk = text_content.replace(' ','')

with open('output.txt', 'w') as file:
    # file.write(text_bulk)
    file.write(text_content)

with open('links.txt', 'w') as file:
    for link in links:
        file.write(link['href'] + '\n')
# print(soup.prettify())  # View the parsed HTML structure
