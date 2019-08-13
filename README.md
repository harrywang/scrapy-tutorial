# Scrapy Tutorial

This tutorial is based on the [Scrapy official tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html) with more information and code on storing data in database using SQLAlchemy.

The webiste to crawl is [http://quotes.toscrape.com](http://quotes.toscrape.com).

<img width="821" alt="Screen Shot 2019-08-13 at 9 43 34 AM" src="https://user-images.githubusercontent.com/595772/62946721-3bb2a280-bdaf-11e9-9521-3f1be57a1838.png">

Local outputs (json and html pages) are stored in "local-output" folder, which is ignored in .gitignore.

For example:

- `scrapy crawl quotes` saves a set of html pages to /local_output
- `scrapy crawl quotes -o ./local_output/quotes.json` saves the output to a json file


## Setup
Tested with Python 3.6 via virtual environment:
```shell
$ python3.6 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
To create the initial project folder, run `scrapy startproject tutorial` (only need to do this once) I removed the top level `tutorial` folder and add additional files and folders as shown below:

```
tutorial/
    scrapy.cfg            # deploy configuration file


    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        models.py         # project database schema file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```



## Run

Run `scrapy crawl quotes` at the project top level.

Note that spider name is defined in the spider class, e.g., `quotes_spider.py`:
```python
class QuotesSpider(scrapy.Spider):
    name = "quotes"
```

## Scrapy Shell


Enter shell: `scrapy shell 'http://quotes.toscrape.com/page/1/'`

Extract data examples (css and xpath)：

CSS：
```bash
>>> response.css('title').getall()
['<title>Quotes to Scrape</title>']
>>> response.css('title::text').get()
'Quotes to Scrape'
>>> response.css('title::text')[0].get()
'Quotes to Scrape'
>>> response.css('title::text').re(r'Quotes.*')
['Quotes to Scrape']
>>> response.css('title::text').re(r'Q\w+')
['Quotes']
>>> response.css('title::text').re(r'(\w+) to (\w+)')
['Quotes', 'Scrape']
```
XPath：

```bash
>>> response.xpath('//title')
[<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
>>> response.xpath('//title/text()').get()
'Quotes to Scrape'
```

View page in browser from shell: `>>> view(response)`

### Extracting quotes and authors

HTML to parse:

```html
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```

Parse and output to log:

```python
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
```
Save the output above to json: `scrapy crawl quotes -o quotes.json` - Note: this command appends to existing json instead of overwriting it.

### Following links

Next link html on the page:

```html
<ul class="pager">
    <li class="next">
        <a href="/page/2/">Next <span aria-hidden="true">&rarr;</span></a>
    </li>
</ul>
```
Extract it via shell:

```bash
>>> response.css('li.next a::attr(href)').get()
'/page/2/'
>>> response.css('li.next a').attrib['href']
'/page/2'
```
Follow links:

```python
for a in response.css('li.next a'):
    yield response.follow(a, callback=self.parse)
```

## Using spider arguments
See https://docs.scrapy.org/en/latest/topics/spiders.html#spiderargs


## Database




## What else?

See: https://docs.scrapy.org/en/latest/intro/overview.html#topics-whatelse
