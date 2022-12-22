# reddit-background

Automatically get the latest images from a subreddit of your choice. Allowing a new desktop image every day. It is a rewrite of [rconradharris/reddit-background](https://github.com/rconradharris/reddit-background), updating it to Python 3.

## Behaviour

The script, when ran will go to the subreddit of your choice (the default is /r/EarthPorn), downloads a number of images and save them to a folder of your choice.

You should set up your Desktop background to watch and update your background accordingly.

## Installation

1. Clone this repository to a location of your choice. `gh repo clone chriscn/reddit-background`
2. Install the requirements of the project. `pip install -r requirements.txt`
3. Adjust the `config.yml` file with your appropriate values.
4. Setup a crontab to fire the script, open with `crontab -e` and paste the following `0 9 * * * python3 /Users/<username>/reddit-background/reddit-background.py --config /Users/<username>/reddit-background/config.yml` 
