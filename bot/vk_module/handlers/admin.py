from typing import Optional
from vkbottle import GroupEventType, CtxStorage, ABCRule
from vkbottle.bot import rules, BotLabeler, Message, MessageEvent
from vkbottle.dispatch.rules.base import CommandRule

from bot.misc.env import VK
from bot.vk_module import answers
from bot.vk_module.config import bot_vk, api
from bot.vk_module.database import Select, Update
from bot.vk_module.keyboards import Reply, Inline
from bot.vk_module.spamming import Spammer, SpamMessage

AnswerText = answers.Text
AnswerCallback = answers.Callback

admin_labeler = BotLabeler()
ctx_user_storage = CtxStorage()
admin_labeler.auto_rules = [rules.FromPeerRule(list(VK.ADMIN_LIST))]


class SelectSpamTableRule(ABCRule[MessageEvent]):
    async def check(self, event: MessageEvent) -> bool:
        return event.payload.get('select_spam_table') is not None


@admin_labeler.message(CommandRule("show_keyboard"))
async def show_keyboard(message: Message) -> None:
    """ Отобразить клавиатуру """
    await message.answer("Вывод клавиатуры", keyboard=Reply.default())


@admin_labeler.message(text="Личный кабинет")
async def personal_area_text(message: Message, event: Optional[MessageEvent] = None, edit_text: bool = False) -> None:
    """ Личный кабинет """
    user_id = message.peer_id
    spam_table_id = Select.spam_config_by_admin_id(user_id).fetchone()

    if spam_table_id is None:
        spam_table_name = 'Таблица не задана'
    else:
        spam_table = Select.spam_table(spam_table_id=spam_table_id['spam_table_id']).fetchone()
        spam_table_name = spam_table['spam_table_name']

    text = "AnswerText.personal_area()"
    keyboard = Inline.personal_area(spam_table_name)

    if edit_text:
        if event is not None:
            await event.edit_message(text, keyboard=keyboard)
    else:
        await message.answer(text, keyboard=keyboard)


@admin_labeler.message(CommandRule("personal_area"))
async def personal_area_command(message: Message) -> None:
    """ Личный кабинет (Command) """
    await personal_area_text(message)


# @admin_router.raw_event(OtherCallback.filter(F.action == "personal_area"))
@admin_labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent, rules.PayloadRule({"cmd": "personal_area"}))
async def personal_area_callback(event: MessageEvent) -> None:
    """ Личный кабинет (Callback) """
    await personal_area_text(event.object, event=event, edit_text=True)


@admin_labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent, rules.PayloadRule({"cmd": "view_spam_tables"}))
async def view_spam_tables(event: MessageEvent) -> None:
    """ Вывести список таблиц для рассылки """
    spam_table_list = Select.spam_table().fetchall()
    if len(spam_table_list) > 0:
        await event.edit_message(
            message="AnswerText.view_spam_tables()",
            keyboard=Inline.view_spam_tables(spam_table_list)
        )
    else:
        await event.answer(message="Таблицы отсутствуют")


@admin_labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent, SelectSpamTableRule())
async def select_spam_table(event: MessageEvent) -> None:
    """ Выбрать таблицу для рассылки из списка """
    user_id = event.object.peer_id
    spam_table_id = event.payload.get('select_spam_table')
    spam_table = Select.spam_table(spam_table_id=spam_table_id).fetchone()

    if spam_table is not None:
        spam_table_name = spam_table['spam_table_name']
        Update.spam_config_table(user_id, spam_table_id)
        await event.show_snackbar(f"Вы выбрали таблицу: «{spam_table_name}» ({spam_table_id})")
    else:
        await event.show_snackbar(f"Такой таблицы не существует")

    await personal_area_callback(event)


@admin_labeler.message(text="/start <text>")
async def start_spam(message: Message, text: Optional[str] = None) -> None:
    """ Произвести рассылку """
    user_id = message.peer_id
    spam_table_id = Select.spam_config_by_admin_id(user_id).fetchone()['spam_table_id']

    if spam_table_id is not None:
        spam_table = Select.spam_table(spam_table_id=spam_table_id).fetchone()
        spam_table_title = spam_table['title']
        user_ids = [int(x['user_id']) for x in Select.user_ids_for_spamming(spam_table_title).fetchall()]

        spam_message = SpamMessage()
        spam_message.text = text

        await message.answer(spam_message.text)
        await Spammer(api).start(user_ids, spam_message)
    else:
        await message.answer("Вы не задали таблицу для рассылки!")


@admin_labeler.message(text="/test <text>")
async def test_spam(message: Message, text: Optional[str] = None) -> None:
    """ Тестовая рассылка (только отправителю) """
    await message.answer(text)


@admin_labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent, rules.PayloadRule({"cmd": "close"}))
async def close_window(event: MessageEvent) -> None:
    """ Закрыть окно (удалить сообщение) """
    await bot_vk.api.messages.delete(
        peer_id=event.object.peer_id,
        message_ids=[event.object.conversation_message_id]
    )
