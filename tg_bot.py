import json
from aiogram import Bot, Dispatcher, executor, types

import scrap_av
from config import token

bot = Bot(token=token)
db = Dispatcher(bot)


@db.message_handler(commands='set.filter')
async def set_filter(message: types.Message):
    await message.answer('Enter your car settings')


@db.message_handler(commands='start')
async def start(message: types.Message):
    scrap_av.AVScrapper().parse()

    with open('av_cars.json') as file:
        cars_from_file = json.load(file)

    for k, car_data in cars_from_file.items():
        cars = f'{car_data.get("article_url")}'

        await message.answer(cars)


if __name__ == '__main__':
    executor.start_polling(db)
