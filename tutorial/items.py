# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip(u'\u201c'u'\u201d')
    return text




class QuoteItem(Item):
    quote_content = Field(
        input_processor=MapCompose(remove_quotes),
        # TakeFirst return the first value not the whole list
        output_processor=TakeFirst()
        )
    author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    tags = Field()
