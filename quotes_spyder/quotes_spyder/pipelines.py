from itemadapter import ItemAdapter
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .models import Author, KeyWord, Quote, Base

class QuotesSpyderPipeline:
    def process_item(self, item, spider):
        return item


class SqliteDemoPipeline:
    pass

    def __init__(self):

        engine = create_engine("sqlite:///quotes.db", connect_args={'check_same_thread': False}, poolclass=StaticPool)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def process_item(self, item, spider):

        author = item["author"][0]
        try:
            author_to_add = self.session.query(Author).filter_by(name=str(author)).first()
            if (author_to_add.birth == None) and item.get("born", None):
                author_to_add.birth = item["born"]

        except:
            birthday = item.get("born", None)
            author_to_add = Author(name=author, birth=birthday, link=item["author_ref"])

        #keywords check
        key_words_list = []
        
        for kw in item["keywords"]:

            try:
                key_to_add = self.session.query(KeyWord).filter(name=kw)
            except:
                key_to_add = KeyWord(name=kw)   
            key_words_list.append(key_to_add)

        quote_text = Quote(name=item["quote"])
        quote_text.author = author_to_add
        quote_text.keywords = key_words_list


        self.session.add(quote_text)
        self.session.commit()
        return item
