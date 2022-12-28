from django.shortcuts import render
from .models import Log


def index(request):
    """The home page for Learning Log."""
    template = 'home.html'
    context = {'text': 'Hello World', }
    return render(request, template, context)


def logs(request):
    """Show all logs."""
    logs = Log.objects.order_by('date_added')
    template = 'logs/logs_list.html'
    context = {'logs': logs}
    return render(request, template, context)


def log(request, pk):
    """Show a single log and all its entries."""
    template = 'logs/log.html'
    context = {'log': Log.objects.get(id=pk)}
    return render(request, template, context)
