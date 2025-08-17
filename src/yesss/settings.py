# -*- coding: utf-8 -*-

# Scrapy settings for yesss project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = "yesss"

SPIDER_MODULES = ["yesss.spiders"]
NEWSPIDER_MODULE = "yesss.spiders"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

ITEM_PIPELINES = {
    "yesss.pipelines.YesssPipeline": 10,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0"

BASE_LOCATION = "/tmp/yesss/"
