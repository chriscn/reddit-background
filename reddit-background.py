import argparse
import logging
import sys
import yaml
import requests
import nanoid
import os
from voluptuous import Schema, Required, All, Length, Any, MultipleInvalid, IsDir

config_schema = Schema({
    Required('subreddit'): All(str, Length(min=1, max=20)),
    Required('sort'): Any('top', 'hot'),
    'period': Any('hour', 'week', 'month', 'year', 'all'),
    Required('amount'): int,
    Required('output'): IsDir()
})


def clear_dir(dir):
    file_list = [f for f in os.listdir(dir) if f.endswith(".jpg")]
    for f in file_list:
        os.remove(os.path.join(dir, f))


def download_image(url):
    with open(f'backgrounds/{nanoid.generate()}.jpg', 'wb') as file:
        file.write(requests.get(url).content)


def main():
    parser = argparse.ArgumentParser(description='Automatically download images from Reddit to use on your desktop.')
    parser.add_argument('--config', type=argparse.FileType('r'), required=True)

    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    args = parser.parse_args()
    config = yaml.safe_load(args.config)

    try:
        config_schema(config)
    except MultipleInvalid as e:
        logging.error(f'Configuration valid does not match schema: {str(e)}')
        logging.error(e)
        sys.exit(1)

    logging.info(f"Removing all jpg files in directory: {config.get('output')}")
    clear_dir(config.get('output'))

    url = f"https://reddit.com/r/{config.get('subreddit')}/{config.get('sort')}.json"
    logging.info(f'Using URL {url}')

    subreddit = requests.get(url, headers={'User-Agent': 'github/chriscn/reddit-background'}, timeout=10).json()

    for i in range(0, config['amount'] - 1):
        download_image(subreddit['data']['children'][i]['data']['url'])


if __name__ == '__main__':
    main()
