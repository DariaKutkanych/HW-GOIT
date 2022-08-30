from sqlalchemy import Column, Integer, String


from db import Base, engine


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    source = Column(String(50), nullable=False)


Base.metadata.create_all(engine)