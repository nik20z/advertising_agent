from _datetime import datetime
from typing import List
from vkbottle import API, VKAPIError

from bot.vk_module.config import logger


class SpamMessage:
    """ Класс сообщения для рассылки"""

    text: str = ''


class Spammer:
    """ Класс для рассылки сообщений """

    def __init__(self, api: API):
        self.api = api

    async def start(self, user_ids: List[int], spam_message: SpamMessage) -> None:
        for user_id in user_ids:
            try:
                await self.api.messages.send(
                    user_id=user_id,
                    message=spam_message.text,
                    random_id=int(datetime.now().timestamp())
                )
            except VKAPIError as e:
                logger.info(f"{e.code}: {e.description}")

