import json
import codecs
import requests
from datetime import datetime
import time


def parse():
    page = get_page()
    return get_raw_data(page=page)


def get_page():
    settings_list = set_params_for_search()

    post_json = {
        "properties": [
            {
                "name": "price_currency",
                "value": 2
            },
            {
                "name": "creation_date",
                "value": 10
            },
            {
                "value": settings_list.get('year'),
                "name": "year"
            },
            {
                "value": settings_list.get('transmission_type'),
                "name": "transmission_type"
            }
        ],

        "sorting": 4
    }

    request_data = requests.post(url='https://api.av.by/offer-types/cars/filters/main/apply', json=post_json)
    return request_data.json()


def get_raw_data(page: requests):
    raw_page = page
    cars_dict = {}

    for article_i in range(5):
        iso_time = datetime.fromisoformat(raw_page.get('adverts')[article_i].get('publishedAt')[:-5])
        iso_time = datetime.strftime(iso_time, '%Y-%m-%d %H:%M:%S')
        d_timestamp = time.mktime(datetime.strptime(iso_time, '%Y-%m-%d %H:%M:%S').timetuple())

        cars_dict[raw_page.get('adverts')[article_i].get("id")] = {
            'brand': raw_page.get('adverts')[article_i].get('properties')[0].get('value'),
            'model': raw_page.get('adverts')[article_i].get('properties')[1].get('value'),
            'generation': raw_page.get('adverts')[article_i].get('properties')[2].get('value'),
            'year': raw_page.get('adverts')[article_i].get('properties')[3].get('value'),
            'engine_capacity': raw_page.get('adverts')[article_i].get('properties')[4].get('value'),
            'fuel_type': raw_page.get('adverts')[article_i].get('properties')[5].get('value'),
            'transmission_type': raw_page.get('adverts')[article_i].get('properties')[6].get('value'),
            'price_usd': raw_page.get('adverts')[article_i].get('price').get('usd').get('amount'),
            'price_byn': raw_page.get('adverts')[article_i].get('price').get('byn').get('amount'),
            'article_url': raw_page.get('adverts')[article_i].get('publicUrl'),
            'd_timestamp': d_timestamp
        }

    return cars_dict


def set_params_for_search():
    settings_dict = {
        'brand': 'Mazda',
        'Model': 6,
        'year': '',
        'transmission_type': '1'
    }
    return settings_dict


def save_data(path: str, data: dict[any]):
    with codecs.open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def main():
    data = parse()
    save_data(path='av_cars.json', data=data)


if __name__ == '__main__':
    main()

