from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import Dict
import json
import codecs
from uuid import uuid4
import requests

@dataclass
class CarInfo:
    brand: str
    model: str
    generation: str
    year: str
    engine_capacity: str
    fuel_type: str
    transmission_type: str
    price_usd: str
    price_byn: str
    article_url: str
    car_id: uuid4 = field(default_factory=uuid4)

class ScrapperFacade(ABC):

    def parse(self):
        page = self.get_page()
        raw_data = self.get_raw_data(page=page)
        return self.clear_data(raw_data)

    @abstractmethod
    def get_page(self) -> str:
        """Make request for getting html, xml or json data.
        It should be safe. Don't forget to wrap in try-except block."""

    @abstractmethod
    def get_raw_data(self, page: str):
        """Make dict with raw data."""

    @abstractmethod
    def clear_data(self, adverts_dict: Dict):
        """Make dict with raw data."""


class AVScrapper(ScrapperFacade):

    def __init__(self):
        self.av_list = {
            'brand': 'Mazda',
            'Model': 6,
            'year': '',
            'transmission_type': '1'
        }

        self.json = {
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
                    "value": self.av_list.get('year'),
                    "name": "year"
                },
                {
                    "value": self.av_list.get('transmission_type'),
                    "name": "transmission_type"
                }
            ],

            "sorting": 4
        }

    def get_page(self):
        return requests.post(url='https://api.av.by/offer-types/cars/filters/main/apply', json=self.json).json()

    def get_raw_data(self, page: str):
        return page.get('adverts')

    def clear_data(self, adverts_dict: Dict):
        cars_dict = {}

        for article in adverts_dict:
            cars_dict[article.get("id")] = {
                'brand': article.get('properties')[0].get('value'),
                'model': article.get('properties')[1].get('value'),
                'generation': article.get('properties')[2].get('value'),
                'year': article.get('properties')[3].get('value'),
                'engine_capacity': article.get('properties')[4].get('value'),
                'fuel_type': article.get('properties')[5].get('value'),
                'transmission_type': article.get('properties')[6].get('value'),
                'price_usd': article.get('price').get('usd').get('amount'),
                'price_byn': article.get('price').get('byn').get('amount'),
                'article_url': article.get('publicUrl'),
            }

        return cars_dict


def save_data(path: str, data):
    with codecs.open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    av_scrapper = AVScrapper()
    data = av_scrapper.parse()
    save_data(path='av_cars.json', data=data)
