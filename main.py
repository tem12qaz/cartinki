import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import ChatType
from aiogram.utils.executor import set_webhook
from aiohttp import web

from config import BOT_TOKEN, HOST
from image import Image

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE), content_types=['photo', 'document'])
async def handle_photo(message: types.Message):
    if message.document:
        photo = message.document
        if 'jpg' not in photo['mime_type'] and \
                'jpeg' not in photo['mime_type'] and \
                'png' not in photo['mime_type']:
            await message.delete()
            return
    else:
        photo = message.photo[-1]

    name = f'files/{message.message_id}_{photo.file_id}.jpg'
    await photo.download(destination=name)
    img = Image(name, contrast=-20, brightness=-50, gamma=1.7)
    print('---------')

    img.scale_and_bw(*list(map(int, message.caption
                               .split(' '))))
    print('---------')

    text = img.apply_colors()
    print('---------')
    os.remove(name)
    await message.answer(
        text
    )


async def on_startup(dp):
    await dp.bot.set_webhook(HOST + '/' + BOT_TOKEN)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    aiohttp_app = web.Application(loop=loop)

    executor = set_webhook(
        dispatcher=dp,
        webhook_path='/' + BOT_TOKEN,
        loop=loop,
        on_startup=on_startup,
        web_app=aiohttp_app,
    )
    executor.run_app(loop=loop, port=8081)
