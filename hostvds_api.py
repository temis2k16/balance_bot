import requests
import asyncio
from dotenv import load_dotenv
import os

class HostVdsInfo:
    def __init__(self):
        load_dotenv()
        self._user = os.getenv('HOSTVDS_USER')
        self._password = os.getenv('HOSTVDS_PASS')
        self.data = {}
        self.notification = False
        self.notification_threshold = 1.0
        self._refresh_interval = 86400 # 1 day in seconds


    async def refresh_data(self):
        while True:
            await self.login()
            await asyncio.sleep(self._refresh_interval)

    async def login(self):
        r = requests.post("https://hostvds.com/api/login/", json={"email": self._user, "password": self._password})
        self.data = r.json()
    
    async def get_balance(self):
        if not self.data:
            await self.login()
        return self.data['balance']

    def set_balance_notification_threshold(self, amount: float):
        self.notification_threshold = amount

    def enable_notifications(self, enable: bool):
        self.notification = enable