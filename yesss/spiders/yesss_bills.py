# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

from yesss.items import YesssBillItem


class AidaBillsSpider(scrapy.Spider):
    name = ''
    allowed_domains = []
    start_urls = ()
    request_after_login_url = ''

    def __init__(self, username=None, password=None, *args, **kwargs):
        super(AidaBillsSpider, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def parse(self, response):
        if self.username is None or self.password is None:
            self.log('Username or password not provided!', level=scrapy.log.ERROR)
            return

        return scrapy.FormRequest.from_response(
            response,
            formname='loginform',
            formdata={
                'login_rufnummer': self.username,
                'login_passwort': self.password
            },
            callback=self.logged_in
        )

    def logged_in(self, response):
        return scrapy.Request(self.request_after_login_url, callback=self.parse_bills)

    def parse_bills(self, response):
        for row in response.xpath('//tbody/tr'):
            bill_item = YesssBillItem()
            bill_item['date_raw'] = row.xpath('td[contains(@data-title, "Datum")]/text()').extract()[0]
            bill_item['date'] = datetime.strptime(bill_item['date_raw'], "%d.%m.%Y")
            bill_item['date_formatted'] = bill_item['date'].strftime('%Y%m%d')
            bill_item['bill_sum'] = row.xpath('td[contains(@data-title, "Summe")]/text()').extract()[0]
            bill_item['bill_no'] = row.xpath('td[contains(@data-title, "Nr")]/text()').extract()[0]
            bill_item['bill_pdf'] = row.xpath('td[contains(@data-title, "Details")]/a/@href').extract()[0]
            bill_item['egn_pdf'] = None
            bill_item['egn_csv'] = None

            egn = row.xpath('td[contains(@data-title, "Einzelgespr")]/a/@href').extract()
            if egn:
                bill_item['egn_pdf'] = egn[0]
                bill_item['egn_csv'] = egn[1]

            yield bill_item


class SimfonieBillsSpider(AidaBillsSpider):
    name = "simfonie-bills"
    allowed_domains = [
        "kontomanager.at",
        "simfonie.at",
    ]
    start_urls = (
        'https://simfonie.kontomanager.at/',
    )
    request_after_login_url = 'https://simfonie.kontomanager.at/rechnungen.php'


class YesssBillsSpider(AidaBillsSpider):
    name = "yesss-bills"
    allowed_domains = [
        "yesss.at",
    ]
    start_urls = (
        'https://www.yesss.at/',
    )
    request_after_login_url = 'https://www.yesss.at/kontomanager.at/rechnungen.php'
