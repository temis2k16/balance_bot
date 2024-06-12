import asyncio

from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
import os

from hostvds_api import HostVdsInfo

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)
vdsinfo = HostVdsInfo()


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = "Это бот HostVDS!\nИспользуйте команду /balance для получения баланса\n"
    await bot.reply_to(message, text)


# Handler for messages containing "balance"
@bot.message_handler(commands=['balance'])
async def get_balance(message):
    balance = await vdsinfo.get_balance()
    await bot.reply_to(message, f"Баланс: {balance} $")


async def main():
    asyncio.create_task(vdsinfo.refresh_data())
    await bot.polling(non_stop=True, interval=2.0)


if __name__ == '__main__':
    asyncio.run(main())