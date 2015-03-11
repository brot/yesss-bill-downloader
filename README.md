# yesss! bill downloader

With this (standalone) scrapy (http://scrapy.org/) spider it's possible to automatically download bills (pdf) and call details (pdf+csv)
from https://www.yesss.at and store in on your local machine.

The files are stored under /tmp/yesss (could be change as commandline option) in the following structure

```
/tmp/
  -- yesss/
     -- <username>
        -- <year>
           -- <date>-rechnung.pdf
           -- <date>-einzelgesprächsnachweis.pdf
           -- <date>-einzelgesprächsnachweis.csv
```

## Prerequisite

First you have to install scrapy on your machine: http://doc.scrapy.org/en/latest/intro/install.html

## Starting the spider

```
user@machine:..../yesss-bills$ scrapy crawl -a username=<username> -a password=<password> -s BASE_LOCATION=<base-location>/ yesss_bills
```

### Parameters

* *username:* username, normally your phonenumber 436xxxxxxxx
* *password:* your password
* *BASE_LOCATION:* base location where you want to store your files
