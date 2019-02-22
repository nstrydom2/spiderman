import requests
import time
import random
import datetime
import os

from bs4 import BeautifulSoup

class Spider():
    def get_urls(self, html_doc):
        soup = BeautifulSoup(html_doc.content, 'lxml')
        urls = []

        for url in soup.find_all('a'):
            try:
                if url.get('href').find("http://") > -1 or url.get('href').find("https://") > -1:
                    print("[*] url found -> " + url.get('href'))
                    urls.append(url.get('href'))

                    self.log_to_file(url)

            except Exception as ex:
                print("[*] Error -> " + str(ex))

        return urls

    def remove_duplicates(self, urls):
        print("[*] Removing duplicates.")

        return list(set(urls))

    def shuffle_urls(self, urls):
        print("[*] Shuffling urls.")

        for num in range(5):
            random.seed(datetime.datetime.now())
            random.shuffle(urls)

        return urls

    def get_tail_log(self, num_of_lines):
        with open('log.txt', 'r') as in_file:
            return in_file.readlines()[num_of_lines * -1:]

    def log_to_file(self, url):
        with open('log.txt', 'a') as out_file:
            out_file.write(url.get('href') + '\n')

    def remove_duplicates_log(self):
        with open('log.txt', 'r') as in_file:
            content = in_file.readlines()

            with open('log.txt', 'w') as out_file:
                out_file.writelines(list(set(content)))

    def go_spidey_go(self, url):
        html_doc = requests.get(url, timeout=5)
        urls = self.shuffle_urls(self.get_urls(html_doc))

        while True:
            for num in range(2**5):
                try:
                    urls = self.shuffle_urls(self.remove_duplicates(urls))

                    for url in urls:
                        print("[*] Request sent to -> " + url)

                        html_doc = requests.get(url, timeout=(5, 5))

                        if html_doc is None:
                            raise Exception("Server return nothing")

                        # Append to the urls list
                        urls += self.get_urls(html_doc)

                        time.sleep(0.4)

                except Exception as ex:
                    print("[*] Error -> " + str(ex))

            self.remove_duplicates_log()
            urls = self.shuffle_urls(self.get_tail_log(1024))



if __name__ == '__main__':
    spidey = Spider()

    start_url = 'https://cnn.com/'

    spidey.remove_duplicates_log()

    # if start_url is None:
    #     with open('log.txt', 'rb') as in_file:
    #         start_url = in_file.readlines()[-1].decode()

    spidey.go_spidey_go(start_url)
