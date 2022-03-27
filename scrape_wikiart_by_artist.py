import urllib.request
import re
from bs4 import BeautifulSoup
import time
import os


image_folder = "images"
base_url = "https://www.wikiart.org"


def consider_painting(painting_soup):
    if "Public domain" not in painting_soup.text:
        return False

    genre = painting_soup.find("span", {"itemprop": "genre"})
    if not genre or genre.text != 'abstract':
        return False

    return True


def extract_work(work, artist_name, idx):
    link = work.find("a")
    if not link or 'href' not in link.attrs:
        return False

    painting_url = base_url + '/' + link.attrs["href"]
    try:
        painting_soup = BeautifulSoup(
            urllib.request.urlopen(painting_url), "html.parser")
    except Exception as e:
        print(f'Cannot open {painting_url} due to {e}')
        return False

    # if not consider_painting(painting_soup):
    #  return False

    og_image = painting_soup.find("meta", {"property": "og:image"})
    image_url = og_image["content"].split(
        "!")[0]  # ignore the !Large.jpg at the end
    save_path = os.path.join(
        image_folder, artist_name + '_' + str(idx) + '.jpg')

    time.sleep(0.2)  # try not to get a 403
    try:
        urllib.request.urlretrieve(image_url, save_path)
    except Exception as e:
        print(f'Cannot download {image_url} due to {e}')
        return False

    print(f'Saved {save_path}.')
    return True


def extract(artist_name):
    #artist_url = base_url + '/en/' + artist_name
    # print(artist_url)
    #artist_soup = BeautifulSoup(urllib.request.urlopen(artist_url), "html.parser")
    # print(artist_soup.text)

    artist_work_url = base_url + '/en/' + artist_name + '/all-works/text-list'
    try:
        artist_work_soup = BeautifulSoup(
            urllib.request.urlopen(artist_work_url), "html.parser")
    except Exception as e:
        print('Cannot open {artist_work_url} due to {e}')
        return 0

    works = artist_work_soup.find('main').find_all("li")
    print(f'{len(works)} works by {artist_name}')

    image_count = 0
    for work in works:
        if extract_work(work, artist_name, image_count):
            image_count += 1

    print(f'{image_count} images saved for {artist_name}.')
    return image_count


def main():
    artist_names = [
        # 'alexander-calder',
        'ellsworth-kelly',
    ]
    for artist_name in artist_names:
        num_saved = extract(artist_name)


if __name__ == '__main__':
    main()
