# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm import sessionmaker
from tutorial.models import Quote, Author, Tag, db_connect, create_table

class SaveQuotesPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
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

        for tag_name in item["tags"]:
            tag = Tag(name=tag_name)
            # check whether the current tag already exists in the database
            exist_tag = session.query(Tag).filter_by(name = tag.name).first()
            if exist_tag is not None:  # the current tag exists
                tag = exist_tag
            quote.tags.append(tag)


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
