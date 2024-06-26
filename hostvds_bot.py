import asyncio

from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv
import os

from hostvds_api import HostVdsInfo

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)
vdsinfo = HostVdsInfo()
user_id = 0


# Handle '/start'
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    global user_id
    user_id = message.chat.id
    text = "Это бот HostVDS!\nИспользуйте команду /balance для получения баланса\n"
    await bot.reply_to(message, text)
    asyncio.create_task(vdsinfo.refresh_data(send_balance_notification))


# Handler for messages containing "balance"
@bot.message_handler(commands=['balance'])
async def get_balance(message):
    global user_id
    if user_id != message.chat.id:
        user_id = message.chat.id
    balance = await vdsinfo.get_balance()
    await bot.reply_to(message, f"Баланс: {balance} $")


# Callback for sending notification on low balance
async def send_balance_notification(balance, threshold):
    if user_id != 0:
        await bot.send_message(user_id, 
                           f"Баланс: {balance} $\nБаланс ниже отметки в {threshold} $\n" +
                            "Пополните баланс, чтобы избежать отключения:\n" + 
                            "https://hostvds.com/control/billing/make-payment/pay-with#card-payment")


async def main():
    await bot.polling(non_stop=True, interval=2.0)


if __name__ == '__main__':
    asyncio.run(main())
