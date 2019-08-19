## Scrapinghub Deployment

Create an free account and create a project:
![Screen Shot 2019-08-19 at 11 27 48 AM](https://user-images.githubusercontent.com/595772/63278299-05749780-c275-11e9-9c3f-f750ae5bc6e1.png)

We will use the `shub` command line to deploy. You can find your API key and deploy number once in your project Code & Deploys page:
![Screen Shot 2019-08-19 at 11 33 05 AM](https://user-images.githubusercontent.com/595772/63278652-aebb8d80-c275-11e9-8fb1-1945888d6a53.png)

Go back to the root of Scrapy-tutorial (the root of the Scrapy project) and use the following command to deploy your project to Scrapyinghub.

```bash

(venv) dami:scrapy-tutorial harrywang$ shub login
Enter your API key from https://app.scrapinghub.com/account/apikey
API key: xxxxx
Validating API key...
API key is OK, you are logged in now.
(venv) dami:scrapy-tutorial harrywang$ shub deploy 404937
Messagepack is not available, please ensure that msgpack-python library is properly installed.
Saving project 404937 as default target. You can deploy to it via 'shub deploy' from now on
Saved to /Users/harrywang/xxx/scrapy-tutorial/scrapinghub.yml.
Packing version b6ac860-master
Created setup.py at /Users/harrywang/xxx/scrapy-tutorial
Deploying to Scrapy Cloud project "404937"
{"status": "ok", "project": 4xxx, "version": "b6ac860-master", "spiders": 3}
Run your spiders at: https://app.scrapinghub.com/p/404937/
```
Scrapinghub configuration file is created `scrapinghub.yml` and you need to edit it to specify:

- scrapy 1.7 running Python 3
- requirements files for other packages

```yml
project: 404937

stacks:
    default: scrapy:1.7-py3

requirements:
  file: requirements.txt
```

run `$ shub deploy` to deploy again.

We have three spiders in the project:
- quotes_spider.py is the main spider
- quotes_spider_v1.py is the version 1 of the spider that writes to files, etc.
- authors_spider.py is the spider to get author page from the official tutorial

You can see your current deployment on scrapinghub.com:
![Screen Shot 2019-08-19 at 11 44 31 AM](https://user-images.githubusercontent.com/595772/63279289-bd567480-c276-11e9-8b0d-f24607517652.png)

Then, you can run your spider:

![Screen Shot 2019-08-19 at 12 47 48 PM](https://user-images.githubusercontent.com/595772/63287962-8ccc0600-c289-11e9-9a50-159ccbfb16fe.png)

![Screen Shot 2019-08-19 at 12 48 51 PM](https://user-images.githubusercontent.com/595772/63287944-85a4f800-c289-11e9-9edb-f2e32f8b3a35.png)

Once the job is complete, you can check the results and download the items:
![Screen Shot 2019-08-19 at 1 57 49 PM](https://user-images.githubusercontent.com/595772/63287923-76be4580-c289-11e9-8269-85f156a19a02.png)

![Screen Shot 2019-08-19 at 1 58 22 PM](https://user-images.githubusercontent.com/595772/63288027-b127e280-c289-11e9-858b-7f03b37f721f.png)

You can schedule periodic jobs if you upgrade your free plan.
