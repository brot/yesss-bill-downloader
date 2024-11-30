# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy

from yesss.items import YesssBillItem

CONSENT_COOKIE = {"CookieSettings": '{"categories":["necessary"]}'}


class AidaBillsSpider(scrapy.Spider):
    name = ""
    allowed_domains = []
    start_urls = ()
    request_after_login_url = ""

    def __init__(self, username=None, password=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password

    def parse(self, response):
        if self.username is None or self.password is None:
            self.log("Username or password not provided!", level=scrapy.log.ERROR)
            return

        return scrapy.FormRequest.from_response(
            response,
            formid="loginform",
            formdata={"login_rufnummer": self.username, "login_passwort": self.password},
            callback=self.logged_in,
        )

    def start_requests(self):
        if not self.start_urls and hasattr(self, "start_url"):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)"
            )
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=CONSENT_COOKIE, dont_filter=True)

    def logged_in(self, response):
        # check if login was successful
        if alert_list := response.xpath('//div[@role="alert"]/p/strong[1]/text()'):
            self.logger.error("[%s] %s", self.username, alert_list.get())
            return

        self.logger.info("[%s] Logged in sucessfully and continue on %s", self.username, response.url)
        return scrapy.Request(self.request_after_login_url, cookies=CONSENT_COOKIE, callback=self.parse_bills)

    def parse_bills(self, response):
        self.logger.info("[%s] Parsing bill table on %s", self.username, response.url)
        for row in response.xpath('//ul[@class="list-group mt-3"]'):
            bill_item = YesssBillItem()
            bill_item["date_raw"] = row.xpath("li[1]/div/div[2]/text()").get()
            bill_item["date"] = datetime.strptime(bill_item["date_raw"], "%d.%m.%Y")
            bill_item["date_formatted"] = bill_item["date"].strftime("%Y%m%d")
            bill_item["bill_sum"] = row.xpath("li[2]/div/div[2]/text()").get()
            bill_item["bill_no"] = row.xpath("li[3]/div/div[2]/text()").get()
            bill_item["bill_pdf"] = row.xpath("li[4]/div/div/a/@href").get()
            bill_item["egn_pdf"] = None

            if egn := row.xpath("li[5]/div/div/a/@href").get():
                bill_item["egn_pdf"] = egn

            yield bill_item


class YesssBillsSpider(AidaBillsSpider):
    name = "yesss-bills"
    allowed_domains = [
        "yesss.at",
    ]
    start_urls = ("https://www.yesss.at/kontomanager.at/app/",)
    request_after_login_url = "https://www.yesss.at/kontomanager.at/app/rechnungen.php"
