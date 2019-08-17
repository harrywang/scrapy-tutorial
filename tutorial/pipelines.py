# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from tutorial.models import Quote, Author, Tag, db_connect, create_tables

class SaveQuotesPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save quotes in the database.

        This method is called for every item pipeline component.
        """
        session = self.Session()
        quote = Quote()
        author = Author()
        tag = Tag()
        author.name = item["author_name"][0]
        author.bio = item["author_bio"][0]
        quote.quote_content = item["quote_content"][0]  # content is a list
        quote.author = author

        try:
            session.add(author)
            session.add(quote)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
