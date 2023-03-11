# from threading import Thread

from django.shortcuts import get_object_or_404
from logs.models import Group, Log
from telebot import TeleBot, types

# from learninglogs.settings import DEBUG, TELEGRAM_TOKEN, WEBHOOK_URL
from learninglogs.settings import TELEGRAM_TOKEN


from .bot_keyboards import back_keyboard, groups_keyboard, logs_keyboard
from .callback import GroupsCallbackFilter, groups_factory, logs_factory
from .utils import html_to_telegram

bot = TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def get_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/Группы")
    btn2 = types.KeyboardButton("/Help")
    markup.add(btn1, btn2)
    bot.delete_message(message.chat.id, message_id=message.message_id)
    bot.send_message(
        message.chat.id,
        text="Рад приветствовать Вас на LearningLogs!.",
        reply_markup=markup
    )


@bot.message_handler(commands=['Группы'])
def groups_command_handler(message: types.Message):
    bot.send_message(
        message.chat.id,
        'Группы:',
        reply_markup=groups_keyboard()
    )
    bot.delete_message(message.chat.id, message_id=message.message_id)


@bot.message_handler(commands=['Help'])
def help_command_handler(message: types.Message):
    help_text = 'Используйте кнопки меню для навигации'
    bot.send_message(message.chat.id, text=help_text, parse_mode='HTML')


@bot.callback_query_handler(func=None, config=groups_factory.filter())
def groups_callback(call: types.CallbackQuery):
    callback_data: dict = groups_factory.parse(callback_data=call.data)
    bot.delete_message(
        call.message.chat.id,
        message_id=call.message.message_id
    )
    group = get_object_or_404(Group, pk=int(callback_data['group_id']))
    bot.send_message(
        call.message.chat.id,
        f'Заметки группы: {group.title}',
        reply_markup=logs_keyboard(group)
    )


@bot.callback_query_handler(func=None, config=logs_factory.filter())
def logs_callback(call: types.CallbackQuery):
    callback_data: dict = logs_factory.parse(callback_data=call.data)
    log = get_object_or_404(Log, pk=int(callback_data['log_id']))
    log_text = html_to_telegram(log.text)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=log_text,
        reply_markup=back_keyboard(),
        parse_mode='HTML'
    )


@bot.callback_query_handler(func=lambda c: c.data == 'back')
def back_callback(call: types.CallbackQuery):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Группы:', reply_markup=groups_keyboard()
    )


bot.add_custom_filter(GroupsCallbackFilter())

bot.delete_webhook()


def bot_local_start():
    bot.infinity_polling()


# if DEBUG:
#     t = Thread(target=bot_local_start)
#     t.setDaemon(True)
#     t.start()
# else:
#     bot.set_webhook(url=WEBHOOK_URL)
