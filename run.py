#!/usr/bin/env python3
import argparse
import getpass
import logging
from pathlib import Path
import os
import sys

from pydantic import BaseSettings
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


class Settings(BaseSettings):
    keybase_filepath: str = "~/keys.kdbx"
    keybase_search_path: str = "Root/Allgemein/"
    output_path: str = "/tmp/yesss"

    class Config:
        env_file = ".env"


settings = Settings()

KEEPASS_SEARCH_CRITERIA = [
    {
        "spider_name": "yesss-bills",
        "keepass_search_path": settings.keybase_search_path,
        "url": "https://www.yesss.at/kontomanager.php",
    },
    {
        "spider_name": "simfonie-bills",
        "keepass_search_path": settings.keybase_search_path,
        "url": "https://simfonie.kontomanager.at/",
    },
]

logger = None


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--keyfile",
        dest="keyfile",
        action="store",
        required=False,
        default=settings.keybase_filepath,
        help="Path of your keepass file. (Default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        dest="output_dir",
        action="store",
        required=False,
        default=settings.output_path,
        help="Path to the output directory. (Default: %(default)s)",
    )
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False)
    args = parser.parse_args()

    keyfile = Path(args.keyfile).expanduser()
    if not keyfile.exists():
        parser.error(f'Keyfile "{keyfile}" does not exists.')

    args.keyfile = keyfile
    return args


def get_credentials(keyfile, password):
    try:
        keepass = PyKeePass(keyfile, password=password)
    except CredentialsError as except_inst:
        logger.error(except_inst)
        sys.exit(1)

    entries = []
    for criteria in KEEPASS_SEARCH_CRITERIA:
        logger.debug("Check criteria: %s", criteria)
        group = keepass.find_groups(path=criteria["keepass_search_path"])
        for credentials in keepass.find_entries(url=criteria["url"], group=group):
            entries.append(
                {
                    "spider_name": criteria["spider_name"],
                    "title": credentials.title,
                    "username": credentials.username,
                    "password": credentials.password,
                }
            )
    return entries


def run_spider(credential_list, output_dir):
    project_settings = get_project_settings()
    project_settings.set("BASE_LOCATION", str(Path(output_dir).expanduser()))
    runner = CrawlerRunner(project_settings)

    for credential in credential_list:
        logger.info(f'Add "{credential["title"]}" with number {credential["username"]} for crawling')
        runner.crawl(credential["spider_name"], username=credential["username"], password=credential["password"])


    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())

    reactor.run()


if __name__ == "__main__":
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger = logging.getLogger("yesss-bills")
    logger.debug(args)

    password = getpass.getpass()

    credential_list = get_credentials(args.keyfile, password)
    run_spider(credential_list, args.output_dir)
