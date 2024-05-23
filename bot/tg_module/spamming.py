from typing import List

from aiogram import Bot


class SpamMessage:
    """ Класс сообщения для рассылки"""

    text: str = ''


class Spammer:
    """ Класс для рассылки сообщений """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def start(self, user_ids: List[int], spam_message: SpamMessage) -> None:
        for user_id in user_ids:
            await self.bot.send_message(user_id, text=spam_message.text)
