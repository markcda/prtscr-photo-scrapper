#!/usr/bin/env python

import random
import concurrent.futures
import string
import requests
import sys
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def scrape():
    while True:
        try:
            slug = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            url = "https://prnt.sc/" + slug
            response = requests.get(url, headers=headers)
            content = response.content.decode()
            soup = BeautifulSoup(content, features='lxml')
            ufr = requests.get(soup.img['src'], headers=headers)
            f = open(f'{slug}.png', 'wb')
            f.write(ufr.content)
            f.close()
            print(f'[+] Получен файл {slug}.png')
        except requests.exceptions.MissingSchema:
            print(f'[-] Пропущена схема')


def amount_of_threads():
    if len(sys.argv) < 2:
        sys.exit('Не указано число потоков.')
    return int(sys.argv[1])


def start_threads(thread_amount):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(1, thread_amount + 1):
            executor.submit(scrape)
        print('Потоки запущены.')


def main():
    start_threads(amount_of_threads())


if __name__ == "__main__":
    main()
