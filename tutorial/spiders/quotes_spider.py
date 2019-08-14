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
            loader.add_xpath('quote', ".//span[@class='text']/text()")
            loader.add_xpath('author', './/small//text()')
            loader.add_css('tags', 'div.tags a.tag::text')
            #loader.add_xpath('tags', './/meta[@class="keywords"]/@content')

            # without item loader
            # text = quote.xpath(
            #     ".//span[@class='text']/text()").extract_first()
            # author = quote.xpath(
            #     ".//small//text()").extract_first()
            # tags = quote.css('div.tags a.tag::text').getall()
            #
            # item = QuoteItem()
            # item["quote"] = text
            # item["author"] = author
            # item["tags"] = tags
            # yield item

            yield loader.load_item()


        # go to Next page
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
