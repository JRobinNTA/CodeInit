import json
import requests
from bs4 import BeautifulSoup
text_accumulator = ''
linkarray =[]
with open('./links.txt') as f:
    for line in f:
        linkarray.append(line.strip())
        
        
# print(linkarray[10])


for l in  range(len(linkarray)):
    link = linkarray[l]
    
    # print(link)
    print(link)
    # if True:
    #     continue

    with open('./cookies.json') as f:
        cookies = json.load(f)

    length = len(cookies)

    cookie_passer = dict()
    for i in range(length):
        cookie_passer[cookies[i]['Name raw']] = cookies[i]['Content raw']


    url = f"https://sites.google.com/{link}"
    # url = f"https://sites.google.com//nitc.ac.in/interviewdiaries/home?authuser=1"

    response = requests.get(url, cookies=cookie_passer)
    soup = BeautifulSoup(response.content, "html.parser")
    text = soup.find_all('p')


    text_content = "\n".join([element.get_text() for element in text])

    text_accumulator = text_content + text_accumulator
    # print(text_accumulator)


# text_bulk = text_content.replace(' ','')

with open('output.txt', 'w') as file:
    # file.write(text_bulk)
    file.write(text_accumulator)