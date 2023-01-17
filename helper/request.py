import requests
import os
import xmltodict
from random import shuffle
from lib import log

logger = log.get_logger("http_request.core")
default_headers = {
    'User-Agent': os.environ.get('HEADERS_USER_AGENT')}

def api_get(url, headers=None, xml=False, proxies=None):

    # if set none, use default headers

    if headers is None:
        headers = default_headers
    try:
        if proxies:
            shuffle(proxies)
            proxy = {"https": proxies[0]}
            r = requests.get(url, headers=headers, proxies=proxy, timeout=30)
        else:
            r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 200:
            try:
                if xml:
                    return xmltodict.parse(r.text)
                return r.json()
            except:
                return None
        else:
            print("Error response code: " + str(r.status_code))

    except requests.exceptions.HTTPError:
        logger.error("Http error")
    except requests.exceptions.ConnectionError:
        logger.error("Connection error")
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
    except requests.exceptions.RequestException:
        logger.error("Something else error")