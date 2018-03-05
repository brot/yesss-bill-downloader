# yesss! bill downloader

With this (standalone) scrapy (http://scrapy.org/) spider it's possible to automatically download bills (pdf) and call details (pdf+csv)
from https://www.yesss.at + https://www.simfonie.at/ and store it on your local machine.

The files are stored under /tmp/yesss (could be change by a commandline option or a PATH variable) in the following structure

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

* [KeePassXC](https://keepassxc.org/)
* [pipenv](https://docs.pipenv.org/)

```
$ cd yesss-bill-downloader
$ pipenv --python 3.6 install
```

* Configure your yesss! and/or SIMfonie credentials in your KeePassXC database
* Copy `env-template` to `.env` and change the values
* Update KEEPASS_SEARCH_CRITERIA in run.py (TODO: should be configurable in the future) 

## Starting the spider

```
$ pipenv run python run.py
```
