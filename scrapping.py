from bs4 import BeautifulSoup as bs
import requests
from models import Article
from db import db_session

def get_wp_results():
    url = "https://www.washingtonpost.com/politics/?itid=hp_top_nav_politics"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    stories = soup.find_all("div", attrs={'data-feature-id': 'homepage/story'})
    articles = []

    for story in stories:
        article = {
            "name": story.find("h3").text,
            "description": story.find("p").text,
            "author": story.find_all("a", attrs={'class': ['font-xxxs', 'font-light', 'font--meta-text', 'lh-sm', 'gray-dark', 'hover-blue']})[1].text,
            "source": "Washington Post"
        }
        articles.append(article)
    return articles
        

def get_nt_results():
    url = "https://www.nytimes.com/section/politics"
    response = requests.get(url)
    soup = bs(response.text, "html.parser")

    stories = soup.find_all('li', attrs={'class': 'css-112uytv'})

    articles = []

    for story in stories:
        article = {
        "name":  story.find('h2').text,
        "description": story.find("p").text,
        "author": story.find("span", attrs={'class':'css-1n7hynb'}).text,
        "source": "NY Times"
        }
        articles.append(article)
    return articles

if __name__=="__main__":

    articles = []
    articles.extend(get_nt_results())
    articles.extend(get_wp_results())
    for article in articles:
        data = Article(name=article["name"], author=article["author"], description=article["description"], source=article["source"])
        db_session.add(data)
        db_session.commit()
