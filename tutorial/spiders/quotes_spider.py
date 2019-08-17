import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        #'http://quotes.toscrape.com/page/2/',
    ]


    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
             # pay attention to the dot .// to use relative xpath
            loader.add_xpath('quote_content', ".//span[@class='text']/text()")
            # loader.add_xpath('author', './/small//text()')
            loader.add_css('tags', 'div.tags a.tag::text')
            quote_item = loader.load_item()
            author_url = quote.css('.author + a::attr(href)')[0]
            yield response.follow(author_url, self.parse_author, meta={'quote_item': quote_item})

        # go to Next page
        #for a in response.css('li.next a'):
        #    yield response.follow(a, callback=self.parse)
    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', 'h3.author-title::text')
        loader.add_css('author_bio', '.author-description::text')
        yield loader.load_item()

        # yield {
        #     'name': extract_with_css('h3.author-title::text'),
        #     'birthdate': extract_with_css('.author-born-date::text'),
        #     'bio': extract_with_css('.author-description::text'),
        # }
