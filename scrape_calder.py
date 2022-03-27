import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request
import os
import time
import random


def main():
    #artist_work_url = "https://calder.org/archive/all/works/hanging-mobile/"
    #artist_work_url = "https://calder.org/archive/all/works/monumental-sculpture/"
    #artist_work_url = "https://calder.org/archive/all/works/standing-mobile/"
    artist_work_url = "https://calder.org/archive/all/works/stabile/"

    artist_work_url_req = Request(
        artist_work_url, headers={
            'User-Agent': 'XYZ/3.0'})
    artist_work_soup = BeautifulSoup(
        urllib.request.urlopen(artist_work_url_req), 'html.parser')

    links = artist_work_soup.find_all('a')
    print(f'{len(links)} links')

    image_count = 0
    image_urls = set()
    for link in links:
        painting_url = link.attrs['href']
        try:
            painting_soup = BeautifulSoup(
                urllib.request.urlopen(
                    Request(
                        painting_url,
                        headers={
                            'User-Agent': 'XYZ/3.0'})),
                "html.parser")
        except Exception as e:
            print(f'Cannot open {painting_url} due to {e}')
            continue

        image_url = painting_soup.find(
            "meta", {"property": "og:image"})["content"]
        if image_url in image_urls:
            continue
        tag = painting_url.strip('/').split('/')[-1]
        save_path = os.path.join(
            'images', 'calder_stabile_' + tag + '.jpg')

        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'whatever')
        time.sleep(0.2)  # try not to get a 403
        try:
            opener.retrieve(image_url, save_path)
        except Exception as e:
            print(f'Cannot download {image_url} due to {e}')

        image_urls.add(image_url)
        print(f'{save_path} saved')
        image_count += 1

    print(f'Saved {image_count} images in total')


if __name__ == '__main__':
    main()
