# Billboard Playlist Creator

A Python script to create a Spotify playlist from Billboard charts.

## Description

This script uses the Spotify Web API through the Spotipy API and BeautifulSoup to scrape the Billboard Hot 100 chart and create a Spotify playlist with the top songs.
NOTE: you need to setup an app on the Spotify Developer page to use this script

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `spotipy` library

## Usage

1. Install the required libraries by running `pip install -r requirements.txt`
2. Create a Spotify app and obtain a client ID and client secret. You can use http://localhost:8888/callback as your redirect URI
3. Add your SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI to your environment variables
4. Run the script by executing `python main.py`
5. Follow the prompts to enter your desired billboard date and create the playlist

## Features

- Scrapes the Billboard Hot 100 chart for the top songs
- Creates a Spotify playlist with the top songs
- Allows user to enter a custom date for the chart
- Displays a progress bar while creating the playlist
