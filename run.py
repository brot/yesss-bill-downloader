import argparse
import getpass
from pathlib import Path
import os
import sys

from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsIntegrityError

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


KEYBASE_FILEPATH = os.environ.get('KEYBASE_FILEPATH', '~/keys.kdbx')
KEYBASE_SEARCH_PATH = os.environ.get('KEYBASE_SEARCH_PATH', 'Allgemein/')
OUTPUT_PATH = os.environ.get('OUTPUT_PATH', '/tmp/yesss')

KEEPASS_SEARCH_CRITERIA = [
    {
        'spider_name': 'yesss-bills',
        'keepass_search_path': KEYBASE_SEARCH_PATH,
        'url': 'https://www.yesss.at/kontomanager.php',
    },
    {
        'spider_name': 'simfonie-bills',
        'keepass_search_path': KEYBASE_SEARCH_PATH,
        'url': 'https://simfonie.kontomanager.at/',
    }
]


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--keyfile', dest='keyfile', action='store', required=False,
                        default=KEYBASE_FILEPATH,
                        help='Path of your keepass file. (Default: %(default)s)')
    parser.add_argument('--output', dest='output_dir', action='store', required=False,
                        default=OUTPUT_PATH,
                        help='Path to the output directory. (Default: %(default)s)')
    args = parser.parse_args()

    keyfile = Path(args.keyfile).expanduser()
    if not keyfile.exists():
        parser.error(f'Keyfile "{keyfile}" does not exists.')

    return keyfile, args.output_dir


def get_credentials(keyfile, password):
    try:
        keepass = PyKeePass(keyfile, password=password)
    except CredentialsIntegrityError as except_inst:
        print(except_inst)
        sys.exit(1)

    return [
        {
            'spider_name': criteria['spider_name'],
            'title': credentials.title,
            'username': credentials.username,
            'password': credentials.password,
        }
        for criteria in KEEPASS_SEARCH_CRITERIA
        for credentials in keepass.find_entries(url=criteria['url'],
                                                path=criteria['keepass_search_path'])]


def run_spider(credential_list, output_dir):
    project_settings = get_project_settings()
    project_settings.set('BASE_LOCATION', str(Path(output_dir).expanduser()))
    process = CrawlerProcess(project_settings)

    for credential in credential_list:
        print(f'Add "{credential["title"]}" with number {credential["username"]} for crawling')
        process.crawl(credential['spider_name'], username=credential['username'],
                      password=credential['password'])

    process.start()


if __name__ == '__main__':
    keyfile, output_dir = parse_args()
    password = getpass.getpass()

    credential_list = get_credentials(keyfile, password)
    run_spider(credential_list, output_dir)
