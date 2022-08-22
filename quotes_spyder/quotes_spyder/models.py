from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


quote_author_keywords = Table("quote_author_keywords", Base.metadata, 
                        Column("id", Integer, primary_key=True),
                        Column("quote", Integer, ForeignKey("quotes.id")), 
                        Column("author", Integer, ForeignKey("authors.id")),
                        Column("keyword", Integer, ForeignKey("keywords.id")),)

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    birth = Column(String(250))
    link = Column(String(250), nullable=False)
    quotes = relationship("Quote", cascade="all, delete", backref="author")

class KeyWord(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id, ondelete="CASCADE"))
    keywords = relationship("KeyWord", secondary=quote_author_keywords, backref="keywords")