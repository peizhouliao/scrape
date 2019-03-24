import argparse
import requests
import time

from bs4 import BeautifulSoup

def crawl_page(page_index, white_tags, black_tags, base_url):
    current_page = 'http://bay123.com/forum.php?mod=forumdisplay&fid=40&typeid=38&filter=typeid&typeid=38&page={}.html'.format(
        page_index)
    readOut = requests.get(current_page)
    readOut.raise_for_status()
    readOut.encoding = 'utf-8'
    readSoup = BeautifulSoup(readOut.text, "html.parser")

    print('Relevant posts in page {}'.format(page_index))
    ## find the class for post information
    containers = readSoup.find_all('th', {'class': 'new'})

    for container in containers:
        info = container.find('a', {'class': 's xst'})
        if info:
            try:
                title = info.contents[0]
                blocked = False
                for tag in black_tags:
                    if tag in title:
                        blocked = True
                        break
                if blocked:
                    continue

                tagged = False
                for tag in white_tags:
                    if tag in title:
                        tagged = True

                if tagged:
                    try:
                        url = info.get('href')
                        full_url = base_url + url
                        print('The url for "{}": {}'.format(title, full_url))

                    except:
                        pass

            except:
                pass

def main():
    parser = argparse.ArgumentParser(description='Scraping bay123.com with BeautifulSoup')
    parser.add_argument('-p', '--pages', type = int, help='Number of pages to be scraped', default=10)
    args = vars(parser.parse_args())

    website = 'http://bay123.com/'
    ## whitelited tags for post search
    white_tags = ['Millbrae', 'millbrae', 'San Bruno', 'San bruno', 'san bruno',
                 'Caltrain', 'caltrain', 'Bart', 'bart', '94030', '94066']
    ## blacklisted tags for post search
    black_tags = [u'已租']


    for page_index in range(1, args['pages']+1):
        crawl_page(
            page_index = page_index,
            white_tags = white_tags,
            black_tags = black_tags,
            base_url = website
        )

        # Delay by 2 seconds
        print("\n")
        time.sleep(3)


if __name__ == '__main__':
    main()
