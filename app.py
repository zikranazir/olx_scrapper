import logging
import os
import signal
import sys
import requests
from random import shuffle

from helper.saveData import SaveData
from helper.utils import format_data
from lib import log

from dotenv import load_dotenv

load_dotenv()
logger = log.get_logger('house.olx')
save_data = None
default_headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/74.0.3729.169 Safari/537.36"
}


def crawler_detail(content):
    try:
        data = format_data(content)
        save_data = SaveData()
        save_data.save(data)
        logger.info("Id {} saved in database".format(data['title']))
    except Exception as e:
        logging.error(e)

def get_proxy():
    proxy_array = os.environ.get('proxies').split("|")
    return proxy_array


def main():
    save_data = SaveData()
    url = os.environ.get('url')
    start = int(os.environ.get('start'))
    end = int(os.environ.get('end'))
    proxy = get_proxy()

    for page in range(start, end):
        try:
            link = url.replace("#PAGE#", str(page))
            shuffle(proxy)
            proxies = {"https": proxy[0]}
            req = requests.get(link, headers=default_headers, timeout=30, proxies=proxies)
            if req.status_code == 200:
                contents = req.json()
                for content in contents['data']:
                    if save_data.check_duplicate(content['id']) < 1:
                        crawler_detail(content)
                    else:
                        logger.info("{} with Id {} already tracked".format(content['title'], content['id']))
            else:
                logger.error("Error With Status Code:" + str(req.status_code))
                break

        except Exception as e:
            logging.error(e)

signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))

if __name__ == '__main__':
    main()
