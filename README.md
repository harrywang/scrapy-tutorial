# Scrapy Official Tutorial

This is a Scrapy tutorial at https://docs.scrapy.org/en/latest/intro/tutorial.html

## Setup
Tested with Python 3.6 via virtual environment:
```shell
$ virtualenv venv -p python3.6
$ source venv/bin/activate
$ pip install -r requirements.txt
```
To create the initial project folder, run `scrapy startproject tutorial`:
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

I removed the top level `tutorial` folder shown above.
