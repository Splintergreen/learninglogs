from logs.models import Group
from telebot import types

from .callback import groups_factory, logs_factory


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
