#!/usr/bin/env python3
import argparse
import getpass
import logging
import sys
from pathlib import Path

from pydantic_settings import BaseSettings
from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


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
]



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
    parser.add_argument(
        "-p",
        "--password",
        dest="password",
        action="store",
        default=None,
        help="Password for the keepass file. If not provided, you will be prompted.",
    )
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False)
    args = parser.parse_args()

    keyfile = Path(args.keyfile).expanduser()
    if not keyfile.exists():
        parser.error(f'Keyfile "{keyfile}" does not exists.')

    args.keyfile = keyfile
    return args


def get_credentials(keyfile, password):
    logger = logging.getLogger("yesss-bills")
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
    logger = logging.getLogger("yesss-bills")
    project_settings = get_project_settings()
    project_settings.set("BASE_LOCATION", str(Path(output_dir).expanduser()))
    process = CrawlerProcess(project_settings)

    for credential in credential_list:
        logger.info(f'Add "{credential["title"]}" with number {credential["username"]} for crawling')
        process.crawl(credential["spider_name"], username=credential["username"], password=credential["password"])

    # The script will block here until all crawling jobs are finished
    process.start()


def main():
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    logger = logging.getLogger("yesss-bills")  # Configure root logger for the app
    logger.debug(args)

    password = args.password or getpass.getpass("KeePass Password: ")

    try:
        credential_list = get_credentials(args.keyfile, password)
        if credential_list:
            run_spider(credential_list, args.output_dir)
        else:
            logger.warning("No credentials found for the specified criteria. Nothing to do.")
    except CredentialsError:
        # The error is already logged in get_credentials, so we can exit gracefully.
        pass


if __name__ == "__main__":
    main()
