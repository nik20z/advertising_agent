from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.tg_module import answers
from bot.tg_module.config import bot_tg, logger
from bot.tg_module.database import Update, Select
from bot.tg_module.keyboards import Reply, Inline
from bot.tg_module.keyboards.my_callback import OtherCallback, SelectSpamTableCallback
from bot.tg_module.spamming import SpamMessage, Spammer


AnswerText = answers.Text
AnswerCallback = answers.Callback

admin_router = Router()


@admin_router.message(Command("show_keyboard"))
async def show_keyboard(message: Message) -> None:
    """ Отобразить клавиатуру """
    await message.answer(AnswerText.show_keyboard(), reply_markup=Reply.default())


@admin_router.message(F.text.lower() == "личный кабинет")
async def personal_area_text(message: Message, edit_text: bool = False) -> None:
    """ Личный кабинет """
    spam_table_id = Select.spam_config_by_admin_id(message.chat.id).fetchone()

    if spam_table_id is None:
        spam_table_name = 'Таблица не задана'
    else:
        spam_table = Select.spam_table(spam_table_id=spam_table_id['spam_table_id']).fetchone()
        spam_table_name = spam_table['spam_table_name']

    text = AnswerText.personal_area()
    keyboard = Inline.personal_area(spam_table_name)

    if edit_text:
        await message.edit_text(text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)


@admin_router.message(Command("personal_area"))
async def personal_area_command(message: Message) -> None:
    """ Личный кабинет (Command) """
    await personal_area_text(message)


@admin_router.callback_query(OtherCallback.filter(F.action == "personal_area"))
async def personal_area_callback(callback: CallbackQuery) -> None:
    """ Личный кабинет (Callback) """
    await personal_area_text(callback.message, edit_text=True)


@admin_router.callback_query(OtherCallback.filter(F.action == "view_spam_tables"))
async def view_spam_tables(callback: CallbackQuery) -> None:
    """ Вывести список таблиц для рассылки """
    spam_table_list = Select.spam_table().fetchall()
    if len(spam_table_list) > 0:
        await callback.message.edit_text(
            AnswerText.view_spam_tables(),
            reply_markup=Inline.view_spam_tables(spam_table_list)
        )
    else:
        await callback.answer(AnswerCallback.view_spam_tables_empty())


@admin_router.callback_query(SelectSpamTableCallback.filter(F.spam_table_id))
async def select_spam_table(callback: CallbackQuery, callback_data: SelectSpamTableCallback) -> None:
    """ Выбрать таблицу для рассылки из списка """
    user_id = callback.message.chat.id
    spam_table_id = callback_data.spam_table_id
    spam_table = Select.spam_table(spam_table_id=spam_table_id).fetchone()

    if spam_table is not None:
        spam_table_name = spam_table['spam_table_name']
        Update.spam_config_table(user_id, spam_table_id)
        await callback.answer(AnswerCallback.select_spam_table_successful(spam_table_id, spam_table_name))
    else:
        await callback.answer(AnswerCallback.select_spam_table_empty())

    await personal_area_callback(callback)


@admin_router.message(Command("start"))
async def start_spam(message: Message) -> None:
    """ Произвести рассылку """
    user_id = message.chat.id
    spam_table_id = Select.spam_config_by_admin_id(user_id).fetchone()['spam_table_id']

    if spam_table_id is not None:
        spam_table = Select.spam_table(spam_table_id=spam_table_id).fetchone()
        spam_table_title = spam_table['title']
        user_ids = [int(x['user_id']) for x in Select.user_ids_for_spamming(spam_table_title).fetchall()]
        user_ids.append(user_id)

        spam_message = SpamMessage()
        spam_message.text = message.text.replace('/start', '')

        await message.answer(spam_message.text)
        await Spammer(bot_tg).start(user_ids, spam_message)
    else:
        await message.answer(AnswerText.start_spam_table_exist())


@admin_router.message(Command("test"))
async def test_spam(message: Message) -> None:
    """ Тестовая рассылка (только отправителю) """
    await message.answer(message.text.replace('/test', ''))


@admin_router.callback_query(OtherCallback.filter(F.action == "close"))
async def close_window(callback: CallbackQuery) -> None:
    """ Закрыть окно (удалить сообщение) """
    await callback.message.delete()
