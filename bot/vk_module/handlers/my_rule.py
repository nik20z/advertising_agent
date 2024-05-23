from vkbottle import ABCRule
from vkbottle.bot import MessageEvent


class SelectSpamTableRule(ABCRule[MessageEvent]):
    async def check(self, event: MessageEvent) -> bool:
        return event.payload.get('select_spam_table') is not None
