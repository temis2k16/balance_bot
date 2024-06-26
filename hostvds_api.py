import requests
import asyncio
from dotenv import load_dotenv
import os
from typing import Tuple
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='balance_bot.log', encoding='utf-8', level=logging.DEBUG)


class HostVdsInfo:
    def __init__(self):
        load_dotenv()
        self._user = os.getenv('HOSTVDS_USER')
        self._password = os.getenv('HOSTVDS_PASS')
        self.data = {}
        self.notification_threshold = 1.0
        self._failed_refresh_interfal = 3600 # 1 hour in seconds
        self._success_refresh_interval = 14400 # 4 hours in seconds


    async def refresh_data(self, notify_func):
        while True:
            successful_login, _ = await self.login()
            if successful_login:
                balance = self.data['balance']
                if balance < self.notification_threshold:
                    await notify_func(self.data['balance'], self.notification_threshold)
                await asyncio.sleep(self._success_refresh_interval)
            else:
                logger.info("Failed to get balance data on refresh, sleeping for 1 hour")
                await asyncio.sleep(self._failed_refresh_interfal)


    async def login(self) -> Tuple[bool, int]:
        try:
            r = requests.post("https://hostvds.com/api/login/", json={"email": self._user, "password": self._password})
            self.data = r.json()
            return True, r.status_code
        except:
            logger.error(f"Login return code: {r.status_code}\n")
            return False, r.status_code


    async def get_balance(self):
        successful_login = True
        return_code = 200
        if not self.data:
            successful_login, return_code = await self.login()
        if successful_login:
            return self.data['balance']
        else:
            return f"Не удалось получить баланс (код {return_code})"