import requests
from http import HTTPStatus as status
import string
import os
from bs4 import BeautifulSoup

num_pages = int(input('Enter Page Number: '))
article_type = input('Enter Article Type: ')
root_dir = os.getcwd()

i = 1
while i < num_pages + 1:
    page_name = 'Page_{}'.format(i)
    if not os.path.exists(page_name):
        os.mkdir(page_name)
    i += 1

    headers = {'Accept-Language': 'en-US,en;q=0.9'}

    url ='https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={}'.format(i - 1)
    print(url)
    
    r = requests.get(url,headers=headers)
    os.chdir(page_name)

    if r.status_code == status.OK:
        bs = BeautifulSoup(r.text, 'html.parser')
        for news_article in bs.find_all('article'):
            var = news_article.find('span', attrs={'data-test': 'article.type'}).text
            if var == article_type:
                title = news_article.find('h3', attrs={'class': 'c-card__title'}).text
                for each in string.punctuation:
                    title = title.replace(each, '')
                title = title.strip()
                title = title.replace(' ', '_')

                link = news_article.find('a')['href']
                new_url = 'https://www.nature.com/nature{}'.format(link)

                r1 = requests.get(new_url, headers=headers)
                if r1.status_code == 200:
                    bs1 = BeautifulSoup(r1.text, 'html.parser')
                    article_body = bs1.find('p', attrs={'class': 'article__teaser'}).text
                    new_file = open('{}.txt'.format(title), 'w', encoding='utf-8')
                    new_file.write(article_body)
                    new_file.close()
        print("Content saved.")
        os.chdir(root_dir)
    else:
        print('The URL returned ' + str(r.status_code) + '!')