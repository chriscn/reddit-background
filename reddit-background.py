import argparse
import logging
import yaml
import requests
import nanoid
import os
def clear_dir(directory):
    file_list = [f for f in os.listdir(directory) if f.endswith(".jpg")]
    for f in file_list:
        logging.info(f'Removing file {f}')
        os.remove(os.path.join(directory, f))
def download_image(url):
    with open(f'backgrounds/{nanoid.generate()}.jpg', 'wb') as file:
        logging.info(f'Downloading {url} to {file.name}')
        file.write(requests.get(url).content)
def main():
    parser = argparse.ArgumentParser(description='Automatically download images from Reddit to use on your desktop.')
    parser.add_argument('--config', type=argparse.FileType('r'), required=True,
                        help='Configuration file, have a look at the example provided.')

    logging.basicConfig(format='%(message)s', level=logging.INFO)

    args = parser.parse_args()
    config = yaml.safe_load(args.config)

    logging.info(f"Removing all jpg files in directory: {config.get('output')}")
    clear_dir(config.get('output'))

    url = f"https://reddit.com/r/{config.get('subreddit')}/{config.get('sort')}.json"
    logging.info(f'Using URL {url}')

    subreddit = requests.get(url, headers={'User-Agent': 'github/chriscn/reddit-background'}, timeout=10).json()

    for i in range(0, config.get('amount') - 1):
        download_image(subreddit['data']['children'][i]['data']['url'])


if __name__ == '__main__':
    main()
