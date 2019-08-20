# Scrapy Tutorial

This repo contains the code for my tutorial: A Minimalist End-to-End Scrapy Tutorial (https://medium.com/p/11e350bcdec0).

The webiste to crawl is [http://quotes.toscrape.com](http://quotes.toscrape.com).

## Setup
Tested with Python 3.6 via virtual environment:
```shell
$ python3.6 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Run

Run `scrapy crawl quotes` at the project top level.

Note that spider name is defined in the spider class, e.g., `quotes_spider.py`:
```python
class QuotesSpider(scrapy.Spider):
    name = "quotes"
```

## Versions

I keep different versions for learning purposes using git tags:

### Version 1 (tag v1.0)

Key Concepts: basic spider setup, project folder structure, saving files as json and html files, using Scrap shell，Following links, etc.

Local outputs (json and html pages) are stored in "local-output" folder, which is ignored in .gitignore.

For example:

scrapy crawl quotes saves a set of html pages to /local_output
scrapy crawl quotes -o ./local_output/quotes.json saves the output to a json file



To create the initial project folder, run `scrapy startproject tutorial` (only need to do this once) I removed the top level `tutorial` folder and add additional files and folders as shown below:

```
tutorial/
    scrapy.cfg            # deploy configuration file


    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```
`self.log('Saved file %s' % filename)` outputs to the log console. `yield` also outputs the DEBUG info in the console, e.g.:

<img width="732" alt="Screen Shot 2019-08-13 at 3 30 44 PM" src="https://user-images.githubusercontent.com/595772/62971274-66b4ea80-bddf-11e9-906d-2a7545907cb0.png">


### Version 2 (tag v2.0)

The major change is to use Items.

Why use Items?

- clearly specify the structured data to be collected - a central place to look
- leverage pre and post processors for Items via ItemLoaders (you can also define additional custom processors)
- Use item pipelines to save data to databases (Version 3)
- Better code organization - you know where to look for certain processing code

### Version 3 (tag v3.0)

- Add database support via SQLAlchemy and use Item pipeline to save items into database (sqlite and mysql)
- Add instructions on deploying ScrapingHub.com

Three tables: Authors, Quotes, Tags.

- One-to-Many between Authors and Quotes
- Many-to-Many between Tags and Quotes
- Many-to-Many between Tags and Authors

Database schema is defined in `/tutorial/models.py` file and connection string is specified in `/tutorial/settings.py`.
Add a pipleline file and enable the pipeline in `/tutorial/settings.py` (The number 0-1000 specifies the execution order of the pipelines).

```
ITEM_PIPELINES = {
    'tutorial.pipelines.SaveQuotesPipeline': 300,
}
```

Use the following commands to check local SQLite database. https://sqlitebrowser.org can be used as a GUI tool.

```
$ man sqlite3
$ sqlite3 scrapy_quotes.db
sqlite> .tables
sqlite> .schema quote
sqlite> .quit
```
### Test SQLAlchemy in Shell

Once you setup models and pipelines, you can run `scrapy shell` to test the database part. Just paste the code block below and open sqlite database to check the results.

```python
from sqlalchemy.orm import sessionmaker
from tutorial.models import Quote, Author, Tag, db_connect, create_table
engine = db_connect()
create_table(engine)
Session = sessionmaker(bind=engine)
session = Session()

quote1 = Quote()
author1 = Author()
author1.name = "Linus Torvalds"
author1.bio = "Linus Torvalds is the creator the Linux kernel and Git."
quote1.quote_content = "Talk is cheap. Show me the code."
quote1.author = author1
tag1 = Tag(name="linux")
tag2 = Tag(name="git")
tag3 = Tag(name="simple")
quote1.tags.append(tag1)
quote1.tags.append(tag2)
quote1.tags.append(tag3)

try:
    session.add(author1)
    session.add(quote1)
    session.commit()
except:
    session.rollback()
    raise

quote2 = Quote()
author2 = Author()
author2.name = "Steven Jobs"
author2.bio = "Steven Jobs was the chairman, chief executive officer, and co-founder of Apple Inc."
quote2.quote_content = "Stay Hungry Stay Foolish."
quote2.author = author2
tag4 = Tag(name="inspiring")
tag5 = Tag(name="simple")  # this already exists in the database

# See difference between filter and filter_by at https://bit.ly/2TLvqeV

# exist_tag = session.query(Tag).filter(Tag.name == tag5.name).first()
exist_tag = session.query(Tag).filter_by(name = tag5.name).first()
if exist_tag is not None:  # the current tag exists
    tag5 = exist_tag

quote2.tags.append(tag4)
quote2.tags.append(tag5)

try:

    session.add(author2)
    session.add(quote2)
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()
```
### MySQL

- Install MySQL locally: ``$brew install mysql`, which installs MySQL without password. To start MySQL: `mysql.server start` and then connect: `mysql -u root`.

- Create a local database and related user: `CREATE SCHEMA scrapy_quotes DEFAULT CHARACTER SET utf8mb4 ;`

- `mysqlclient` package is required.

- Comment out MySQL connection string in `settings.py` to use MySQL to store items:

    ```python3
    # SQLite
    # CONNECTION_STRING = 'sqlite:///scrapy_quotes.db'

    # MySQL
    CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
        drivername="mysql",
        user="harrywang",
        passwd="tutorial",
        host="localhost",
        port="3306",
        db_name="scrapy_quotes",
    )
    ```

### Version 4 (tag v4.0)
Deployment to Scrapinghub and ScrapydWeb. See [deployment.md](deployment.md) for details.


## Other Notes

### Scrapy Shell


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
Save the output above to json: `scrapy crawl quotes -o ./local_output/quotes.json` - Note: **this command appends to existing json instead of overwriting it**.

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

### Using spider arguments
See https://docs.scrapy.org/en/latest/topics/spiders.html#spiderargs
