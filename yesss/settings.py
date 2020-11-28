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

ITEM_PIPELINES = {
    "yesss.pipelines.YesssPipeline": 10,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'yesss (+http://www.yourdomain.com)'

BASE_LOCATION = "/tmp/yesss/"
