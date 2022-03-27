import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request
import os
import time
import random

#painting_url = "https://ellsworthkelly.org/work/white-over-black-iii"


def find_the_largest_image(image_srcset):
    max_size = -float('inf')
    result = None
    for src in image_srcset:
        url, size = src.strip().split(' ')
        size = float(size.strip()[:-1])
        if size < max_size:
            continue
        result = url
        max_size = size
    return result


def main():
    artist_work_url = "https://ellsworthkelly.org/work/"

    artist_work_url_req = Request(
        artist_work_url, headers={
            'User-Agent': 'XYZ/3.0'})
    artist_work_soup = BeautifulSoup(
        urllib.request.urlopen(artist_work_url_req), 'html.parser')

    links = artist_work_soup.find_all('img')
    print(f'{len(links)} links')

    image_count = 0
    image_urls = set()
    for link in links:
        if 'srcset' not in link.attrs:
            continue
        image_srcset = link.attrs['srcset'].split(',')
        image_url = find_the_largest_image(image_srcset)
        if image_url in image_urls:
            continue
        print(f'image url {image_url}')
        save_path = os.path.join(
            'images', 'kelly_' + str(image_count) + '.jpg')

        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'whatever')
        time.sleep(0.2)  # try not to get a 403
        try:
            opener.retrieve(image_url, save_path)
        except Exception as e:
            print(f'Cannot download {image_url} due to {e}')

        image_urls.add(image_url)
        image_count += 1
        print(f'{save_path} saved')

    print(f'Saved {image_count} images in total')


if __name__ == '__main__':
    main()
