import telebot
from django.http import Http404, JsonResponse
from django.views import View

from learninglogs.settings import DEBUG

from .bot.bot_run import bot


def process_telegram_event(json_data):
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])


class LearningBotView(View):
    def post(self, request, *args, **kwargs):
        process_telegram_event(request.body.decode('utf-8'))
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):
        if DEBUG:
            return JsonResponse(
                {"ok": "Get request received! But nothing done"}
            )
        raise Http404()
