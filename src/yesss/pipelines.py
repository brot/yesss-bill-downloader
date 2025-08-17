# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from typing import Any, NoReturn

from scrapy.exceptions import DropItem
from scrapy.http import Request, Response
from scrapy.pipelines.media import FileInfo, MediaPipeline
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

BILL_FILENAME = "{}-rechnung.pdf"
EGN_FILENAME = "{}-einzelverbindungsnachweis.{}"


class YesssPipeline(MediaPipeline):
    def get_media_requests(self, item: Any, info: MediaPipeline.SpiderInfo) -> list[Request]:
        """Returns the media requests to download"""
        username = info.spider.username
        year = item["date"].strftime("%Y")
        base_location = info.spider.settings.get("BASE_LOCATION", "/tmp/yesss/")
        location_template = f"{base_location}/{username}/{year}/{{file}}"

        bill_pdf_file = location_template.format(file=BILL_FILENAME.format(item["date_formatted"]))
        if os.path.exists(bill_pdf_file):
            raise DropItem("File {} already exists".format(bill_pdf_file))

        requests = [Request(item["bill_pdf"], meta={"filename": bill_pdf_file})]
        if item["egn_pdf"]:
            egn_pdf_file = location_template.format(file=EGN_FILENAME.format(item["date_formatted"], "pdf"))
            requests.append(Request(item["egn_pdf"], meta={"filename": egn_pdf_file}))
        return requests

    def media_to_download(
        self, request: Request, info: MediaPipeline.SpiderInfo, *, item: Any = None
    ) -> Deferred[FileInfo | None]:
        """Check request before starting download"""
        ...

    def media_failed(self, failure: Failure, request: Request, info: MediaPipeline.SpiderInfo) -> NoReturn: ...

    def media_downloaded(
        self, response, request: Request, info: MediaPipeline.SpiderInfo, *, item: Any = None
    ) -> FileInfo:
        """Handler for success downloads"""
        filename = response.meta["filename"]

        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, "wb") as fileobj:
            fileobj.write(response.body)

    def file_path(
        self,
        request: Request,
        response: Response | None = None,
        info: MediaPipeline.SpiderInfo | None = None,
        *,
        item: Any = None,
    ) -> str: ...
