import telebot
from django.views import View
from django.http import JsonResponse
from learninglogs.settings import DEBUG
from django.http import Http404
from .bot import bot


def process_telegram_event(json_data):
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])


class LearningBotView(View):
    def post(self, request, *args, **kwargs):
        process_telegram_event(request.body.decode('utf-8'))
        # else:
        #     # Process Telegram event in Celery worker (async)
        #     # Don't forget to run it and & Redis (message broker for Celery)!
        #   # Locally, You can run all of these services via docker-compose.yml
        #     process_telegram_event.delay(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        if DEBUG:
            return JsonResponse(
                {"ok": "Get request received! But nothing done"}
            )
        raise Http404()
