from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from db import db_session
from models import Article
from typing import Union



app = FastAPI()


class News(BaseModel):
    name: str
    description: str
    author: str
    source: Union[str, None] = "local"


@app.get("/")
def read_article():
    return {"message": "Hurray!!! Congrats!!! It works!!!"}


@app.get("/news")
def read_article(author: Union[str, None] = None, source: Union[str, None] = None):
    
    if author and source:
        articles = db_session.query(Article).filter(Article.author==author, Article.source==source).all()
    elif author:
        articles = db_session.query(Article).filter(Article.author==author).all()
    elif source:
        articles = db_session.query(Article).filter(Article.source==source).all()
    else:
        articles = db_session.query(Article).all()
    
    result = []
    for article in articles:
        print(article.name)
        result.append({"name": article.name, 
                       "author": article.author, 
                       "description": article.description, 
                       "source": article.source})
    return result


@app.get("/news/{article_id}")
def read_article(article_id: int):
    article = db_session.query(Article).filter(Article.id == article_id).first()
    return {"name": article.name, 
            "author": article.author, 
            "description": article.description, 
            "source": article.source}


@app.get("/descriptions/{article_id}")
def read_article(article_id: int):
    article = db_session.query(Article).filter(Article.id == article_id).first()
    return {"description": article.description}


@app.post("/news")
def create_article(article: News):
    item = Article(name=article.name, description=article.description, author=article.author, source=article.source)
    db_session.add(item)
    db_session.commit()

    return {"name": article.name, 
            "author": article.author, 
            "description": article.description, 
            "source": article.source}
