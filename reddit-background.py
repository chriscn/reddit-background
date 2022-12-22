import argparse
import logging
import yaml
import requests
import nanoid
from voluptuous import Schema, Required, All, Length, Any, MultipleInvalid

config_schema = Schema({
    Required('subreddit'): All(str, Length(min=1, max=20)),
    Required('sort'): Any('top', 'hot'),
    'period': Any('hour', 'week', 'month', 'year', 'all'),
    Required('amount'): All(int, Length(min=1, max=25))
})


def download_image(image):
    with open(f'backgrounds/{nanoid.generate()}.jpg', 'wb') as file:
        file.write(requests.get(image['link']).content)


def main():
    parser = argparse.ArgumentParser(description='Automatically download images from Reddit to use on your desktop.')
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    parser.add_argument('--config', type=argparse.FileType('r'), required=True)

    args = parser.parse_args()

    config = yaml.safe_load(args.config)

    try:
        config_schema(config)
    except MultipleInvalid as e:
        logging.error(f'Configuration valid does not match schema: {str(e)}')

    print(config)

    url = f"https://reddit.com/r/{config.get('subreddit')}/{config.get('sort')}.json"
    logging.info(f'Using URL {url}')

    subreddit = requests.get(url, headers={'User-Agent': 'github/chriscn/reddit-background'}, timeout=10).json()
    print(subreddit['data']['children'])

    image_urls = []

    for i in range(0, config['amount'] - 1):
        image_urls.append({'link': subreddit['data']['children'][i]['data']['url'],
                           'title': subreddit['data']['children'][i]['data']['title']})

    print(image_urls)

    for image in image_urls:
        download_image(image)


if __name__ == '__main__':
    main()
