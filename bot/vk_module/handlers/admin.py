from typing import Optional
from vkbottle import CtxStorage
from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import BaseStateGroup

from bot.vk_module.config import bot, api
from bot.misc.env import VK
from bot.database import Select
from bot.vk_module.keyboards import Reply
from bot.vk_module.spamming import Spammer, SpamMessage


admin_labeler = BotLabeler()
ctx_user_storage = CtxStorage()
admin_labeler.auto_rules = [rules.FromPeerRule(list(VK.ADMIN_LIST))]


class UserStates(BaseStateGroup):
    AWAITING_TABLE_SELECTION = "awaiting_table_selection"


selected_table = None


@admin_labeler.message(command="show")
async def show_spam_table(message: Message) -> None:
    """ Вывести список таблиц в виде кнопок """
    spam_table_list = Select.spam_table(type_table='vk').fetchall()
    await message.answer(
        message="Выберите таблицу",
        keyboard=Reply.select_spam_table(spam_table_list)
    )
    await bot.state_dispenser.set(message.peer_id, UserStates.AWAITING_TABLE_SELECTION)


@admin_labeler.message(state=UserStates.AWAITING_TABLE_SELECTION)
async def select_spam_table(message: Message) -> None:
    """ Получение названия таблицы, выбранной пользователем """
    global selected_table
    spam_table_name = message.text.strip()

    if Select.check_exist_spam_table(spam_table_name).fetchone():
        selected_table = spam_table_name
        await message.answer(f"Вы выбрали таблицу: '{spam_table_name}'")
        await bot.state_dispenser.delete(message.peer_id)
    else:
        await message.answer(f"Таблица '{spam_table_name}' отсутствует")


@admin_labeler.message(text="/start <text>")
async def start_spam(message: Message, text: Optional[str] = None) -> None:
    """ Начать рассылку """
    if selected_table is not None:
        if Select.check_exist_spam_table(selected_table).fetchone():
            user_ids = [int(x['user_id']) for x in Select.user_ids_for_spamming(selected_table).fetchall()]
            spam_message = SpamMessage()
            spam_message.text = text
            await message.answer(spam_message.text)
            await Spammer(api).start(user_ids, spam_message)

    else:
        await message.answer(f"Вы ещё не выбрали таблицу")


@admin_labeler.message(text="/test <text>")
async def test_spam(message: Message, text: Optional[str] = None) -> None:
    """ Тестовая рассылка (только отправителю) """
    await message.answer(text)
