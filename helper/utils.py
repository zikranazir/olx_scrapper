import re
import json

from datetime import datetime
from html.parser import HTMLParser

parser = HTMLParser()

# format data
def format_data(raw):
    result = dict()
    #insert detail parameters value into dictionary
    for param in raw['parameters']:
        if 'values' in param:
            value = [u["value"] for u in param['values']]
        else:
            value = param['value']
        result.update({param['key']: value})

    details = result

    data = {
        'content_id': raw['id'],
        'title': raw['title'],
        'price': int(raw['price']['value']['raw']),
        'kecamatan': get_kecamatan(raw),
        'kabupaten/kota': get_kabupaten(raw),
        'media': get_media(raw),
        'details': details,
        'description': raw['description'],
        'user_id': raw['user_id'],
        'createdAt': get_created_at(raw),
        'display_date': get_display_date(raw),
        'crawledAt': datetime.utcnow()


    }
    return data

def get_media(raw):
    # Get content media and saved in array
    results = []
    for media in raw['images']:
        results.append(media['url'])
    return results


def get_kecamatan(raw):
    # Get Kecamatan(District) where content posted
    kecamatan = raw['locations_resolved']['SUBLOCALITY_LEVEL_1_name']
    return kecamatan


def get_kabupaten(raw):
    # Get Kabupaten/Kota(city) where content posted
    result = raw['locations_resolved']['ADMIN_LEVEL_3_name']
    return result

def get_created_at(raw):
    return datetime.strptime(raw['created_at_first'], "%Y-%m-%dT%H:%M:%S%z")

def get_display_date(raw):
    return datetime.strptime(raw['display_date'], "%Y-%m-%dT%H:%M:%S%z")






