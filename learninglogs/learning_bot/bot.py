from logs.models import Group, Log
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types, TeleBot
from telebot.custom_filters import AdvancedCustomFilter
from django.shortcuts import get_object_or_404
from learninglogs.settings import TELEGRAM_TOKEN, DEBUG, WEBHOOK_URL
from lxml.html.clean import Cleaner
import re


bot = TeleBot(TELEGRAM_TOKEN)
groups_factory = CallbackData('group_id', prefix='groups')
logs_factory = CallbackData('log_id', prefix='logs')


def groups_keyboard():
    groups = Group.objects.order_by('title')
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=group.title,
                    callback_data=groups_factory.new(group_id=group.id)
                )
            ]
            for group in groups if group.logs.exists()
        ]
    )


def logs_keyboard(group):
    logs = group.logs.order_by('date_added')
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=log.description,
                    callback_data=logs_factory.new(log_id=log.id)
                )
            ]
            for log in logs
        ]
    )


def back_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text='⬅',
                    callback_data='back'
                )
            ]
        ]
    )


class GroupsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


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


def html_to_telegram(html):
    allow_tags = [
        'b', 'strong', 'i', 'u',
        'em', 'ins', 's', 'strike',
        'del', 'a', 'code', 'pre',
    ]

    youtube_re = r'<iframe .*src="|".*></iframe>'
    header_re = re.compile(r'<head[^a-z][\s\S]*</head>')

    tg_html = re.sub(r'<(/?)h[1-6](?=\s|>)', r'<\1strong', html)
    tg_html = re.sub(youtube_re, r'', tg_html)
    tg_html = header_re.sub('', tg_html)

    cleaner = Cleaner(
        scripts=True,
        embedded=True,
        meta=True,
        page_structure=True,
        links=True,
        style=True,
        allow_tags=allow_tags
    )
    return cleaner.clean_html(tg_html)[5:-6]


bot.add_custom_filter(GroupsCallbackFilter())

bot.delete_webhook()

if DEBUG:
    bot.infinity_polling()
else:
    bot.set_webhook(url=WEBHOOK_URL)
