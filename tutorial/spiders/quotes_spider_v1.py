import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes_v1"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        #'http://quotes.toscrape.com/page/2/',
    ]
    # long version to implement start_urls array:
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]  # getting the page number from the URL
        filename = 'local_output/' + 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get().strip(u'\u201c'u'\u201d'),  # strip the unicode quotes
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # next_page = response.css('li.next a::attr(href)').get()

        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        # shortcut 1
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

        # shortcut 2
        # for href in response.css('li.next a::attr(href)'):
        #     yield response.follow(href, callback=self.parse)

        # shortcut 3
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
